from .Config import *


class FXData:
    __class__: str = "FXData"
    __slots__: dict = ("keepCSV", "keepGZIP", "castDatatime", "outputCSV", "outputPQT")

    def __init__(self,
                 keepCSV: bool = True,
                 keepGZIP: bool = False,
                 castDatetime: bool = False,
                 outputCSV: bool = False,
                 outputPQT: bool = True) -> None:
        self.keepCSV: bool = keepCSV
        self.keepGZIP: bool = keepGZIP
        self.castDatatime: bool = castDatetime
        self.outputCSV: bool = outputCSV
        self.outputPQT: bool = outputPQT

    def _handleIntemediaryFiles(self) -> None:
        if not self.keepCSV:
            fs = glob.glob(f"{TMP_FOLDER}/*.csv")
            for f in fs:
                os.remove(f)
        if not self.keepGZIP:
            fs = glob.glob(f"{TMP_FOLDER}/*.gz")
            for f in fs:
                os.remove(f)

    def __del__(self) -> None:
        self._handleIntemediaryFiles()

    def getData(self,
                pair: str,
                start_dt: Union[str, datetime, date],
                end_dt: Union[str, datetime, date],
                _type: DataType = DataType.TICK,
                **kwargs):
        if isinstance(start_dt, str):
            start_dt = date.fromisoformat(start_dt)
        if isinstance(end_dt, str):
            end_dt = date.fromisoformat(end_dt)

        if isWeekEnd(start_dt):
            raise Exception("Start date is weekend.")
        if isWeekEnd(end_dt):
            raise Exception("End date is weekend.")

        dStart: Dict[str, int] = {"y": int(start_dt.year), "nw": int(start_dt.isocalendar().week)} # y: year, nw: number of week
        dEnd: Dict[str, int] = {"y": int(end_dt.year), "nw": int(end_dt.isocalendar().week)}
        fq = None
        if "fq" in kwargs:
            if str(kwargs["fq"]) not in Frequency.getAvailableFrequencies():
                raise Exception("Invalid frequency provided")
            fq = kwargs["fq"]

        assert dEnd["y"] >= dStart["y"]
        if dEnd["y"] == dStart["y"]:
            assert dEnd["nw"] >= dStart["nw"]
        else:  # dEnd["y"] > dStart["y"]
            pass

        if pair not in AVAILABLE_SYMBOLS[_type]:
            raise Exception(f"Pair {pair} not available for requested type of data ({_type})")

        rY: list = list(
            range(dStart["y"], dEnd["y"] + 1)) if dEnd["y"] != dStart["y"] else [dStart["y"]]
        rW: list = list(
            range(dStart["nw"], getNumberWeeksPerYear(_yr=dStart["y"]) + 1)) + list(range(1, dEnd["nw"] + 1)) \
            if dEnd["y"] > dStart["y"] \
            else list(range(dStart["nw"], dEnd["nw"] + 1))

        THREADS_POOL: list = []
        d = []
        res: Union[List[Tuple[int, int, pd.DataFrame]], List[None]] = [] # [None] * (len(rY) * len(rW))
        for y in rY:
            for w in rW:
                if (y, w) in d:
                    continue
                if w < dStart["nw"] and y == dStart["y"]:
                    continue
                if w > dEnd["nw"] and y == dEnd["y"]:
                    continue
                print(f"Processing week {y}-{w}") #, end=" ")
                d.append((y, w))
                if len(THREADS_POOL) <= THREADS_POOL_LIMIT:
                    print(f"Processing week {y}-{w}", end=" ")
                    t = threading.Thread(target=self.getTickData if _type == DataType.TICK else self.getCandleData,
                                         kwargs={
                                             "pair": pair,
                                             "yr": y,
                                             "wk": w,
                                             "res": res,
                                             "fq": fq
                                         },
                                         name=f"Processing week {y}-{w}")
                    THREADS_POOL.append(t)
                    t.start()
                else:
                    #print(f"Waiting for joining")
                    _ = [t.join() for t in THREADS_POOL]
                    THREADS_POOL = []
        _ = [t.join() for t in THREADS_POOL]  # Final clean

        # Sorting
        dfs = [df[-1] for df in sorted(res, key=lambda x: (x[0], x[1]))]
        dfs = [df.set_index("dt") for df in dfs]
        fdf: pd.DataFrame = pd.concat(objs=dfs, axis=0)  # Axis 0 --> Rows

        if self.castDatatime:
            fdf["dt"] = pd.to_datetime(fdf["dt"], format="%m-%d-%Y %H:%M:%S.%f")

        output_filename: str = f"out_{start_dt:%m-%d-%Y_%H:%M:%S.%f}_{end_dt:%m-%d-%Y_%H:%M:%S.%f}"
        if self.outputCSV:
            #print("writing csv")
            fdf.to_csv(f"{OUT_FOLDER}/csv/{output_filename}.csv")
        if self.outputPQT:
            import pyarrow as pa
            import pyarrow.parquet as pq
            #print("Writing pqt")
            table = pa.Table.from_pandas(df=fdf)
            pq.write_table(table=table, where=f"{OUT_FOLDER}/parquet/{output_filename}.parquet")
        return fdf

    def getTickData(self, pair: str, yr: Union[str, int], wk: Union[str, int], res: list = [], **kwargs) -> pd.DataFrame:
        config_: Config = Config(pair, yr, wk, DataType.TICK)
        config_.setUrl()
        q = self._getDataFrame(config=config_)
        q.columns = ["dt", "b", "a"]
        res.append((yr, wk, q))
        return q

    def getCandleData(self, pair: str, yr: Union[str, int], wk: Union[str, int], fq: str = Frequency.MINUTE, res: list = [], **kwargs) -> pd.DataFrame:
        config_: Config = Config(pair, yr, wk, DataType.CANDLE, _fq=fq)
        config_.setUrl()
        q = self._getDataFrame(config=config_)
        q.columns = ["dt", *[f"b{sym}" for sym in OHLC], *[f"a{sym}" for sym in OHLC]]
        res.append((yr, wk, q))
        return q

    def _getDataFrame(self, config: Config, p: bool = True) -> Union[pd.DataFrame, None]:
        if not isinstance(config, Config):
            raise Exception("Please enter a valid config.")

        # TODO: Check in-cache files (already downloaded) using glob

        # Constructing the URL
        url: str = config.url
        req = requests.get(url=url, stream=True)
        if req.status_code // 100 != 2:
            #print(req.status_code)
            return pd.DataFrame(columns=range(3 if config.type == DataType.TICK else 9))
            # raise Exception("Error while requesting data")
        else:
            print(req.status_code)

        # Downloading .csv.gz (archived file)
        with open(f"{TMP_FOLDER}/{config.getFilename()}.csv.gz", 'wb') as f:
            for chunk in req.raw.stream(1024, decode_content=False):
                if chunk:
                    f.write(chunk)

        if p:
            # Unzipping .csv.gz into a .csv file (unprocessed CSV)
            with gzip.open(f"{TMP_FOLDER}/{config.getFilename()}.csv.gz", 'rb') as f_in:
                with open(f"{TMP_FOLDER}/{config.getFilename()}.csv", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            # Reading unprocessed/binary CSV file
            fi = open(f"{TMP_FOLDER}/{config.getFilename()}.csv", 'rb')
            data = fi.read()
            fi.close()

            # Processing + Writing CSV file
            fo = open(f"{TMP_FOLDER}/{config.getFilename()}.csv", 'wb')
            fo.write(data.replace(b'\x00', b''))
            fo.close()

            # Reading CSV file
            df = pd.read_csv(filepath_or_buffer=f"{TMP_FOLDER}/{config.getFilename()}.csv",
                             sep=",",
                             on_bad_lines='skip')
            if self.castDatatime:
                df["DateTime"] = pd.to_datetime(df["DateTime"], format="%m-%d-%Y %H:%M:%S.%f")
            return df
        return None
