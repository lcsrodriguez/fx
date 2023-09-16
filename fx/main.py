from datetime import *
from .constants import *
from typing import Union
import requests
import pandas as pd
import gzip
import shutil
import glob
import os


def getNumberWeeksPerYear(_yr: int) -> int:
    """ Function returning the number of weeks within a specified year
    :param _yr: Year
    :return: int
    """
    return int(date(year=_yr, month=12, day=29).isocalendar().week)


class Config:
    __slots__ = ("pair", "yr", "wk", "type", "url_", "fq")

    def __init__(self,
                 _pair: str,
                 _yr: Union[str, int],
                 _wk: Union[str, int],
                 _type: DataType = DataType.TICK,
                 **kwargs) -> None:
        self.pair: str = _pair
        self.yr: Union[str, int] = _yr
        self.wk: Union[str, int] = _wk
        self.type: DataType = _type
        self.url_: str = ""
        self.fq: Union[str, None] = None
        if "_fq" in kwargs:
            if str(kwargs["_fq"]) not in list(Frequency.__annotations__.keys()):
                raise Exception("Invalid frequency provided")
            self.fq = kwargs["_fq"]

    def setUrl(self) -> None:
        dom_: str = url[self.type]
        if self.type == DataType.TICK:
            self.url_: str = f"https://{dom_}/{self.pair}/{self.yr}/{self.wk}.{DATA_FILE_EXTENSION}"
        elif self.type == DataType.CANDLE and self.fq is not None:
            self.url_: str = f"https://{dom_}/{self.fq}/{self.pair}/{self.yr}/{self.wk}.{DATA_FILE_EXTENSION}"

    def getUrl(self) -> str:
        return self.url_

    url = property(fget=getUrl, fset=setUrl)

    def getFilename(self) -> str:
        if self.type == DataType.CANDLE:
            return f"{self.type.value}_{self.pair}_{self.fq}_{self.yr}_{self.wk}"
        return f"{self.type.value}_{self.pair}_{self.yr}_{self.wk}"


class Data:
    __slots__ = ("keepCSV", "keepGZIP", "castDatatime")

    def __init__(self,
                 _keepCSV: bool = True,
                 _keepGZIP: bool = False,
                 _castDatetime: bool = False) -> None:
        self.keepCSV: bool = _keepCSV
        self.keepGZIP: bool = _keepGZIP
        self.castDatatime: bool = _castDatetime

    def _handleIntemediaryFiles(self) -> None:
        if not self.keepCSV:
            fs = glob.glob(f"{OUT_FOLDER}/*.csv")
            for f in fs:
                os.remove(f)
        if not self.keepGZIP:
            fs = glob.glob(f"{OUT_FOLDER}/*.gz")
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
        dStart: Dict[str, int] = {"y": int(start_dt.year), "nw": int(start_dt.isocalendar().week)} # y: year, nw: number of week
        dEnd: Dict[str, int] = {"y": int(end_dt.year), "nw": int(end_dt.isocalendar().week)}

        assert dEnd["y"] >= dStart["y"]
        if dEnd["y"] == dStart["y"]:
            assert dEnd["nw"] >= dStart["nw"]
        else:  # dEnd["y"] > dStart["y"]
            pass

        rY: list = list(
            range(dStart["y"], dEnd["y"] + 1)) if dEnd["y"] != dStart["y"] else [dStart["y"]]
        rW: list = list(
            range(dStart["nw"], getNumberWeeksPerYear(_yr=dStart["y"]) + 1)) + list(range(1, dEnd["nw"] + 1)) \
            if dEnd["y"] > dStart["y"] \
            else list(range(dStart["nw"], dEnd["nw"] + 1))

        isLooping: bool = True
        for y in rY:
            for w in rW:
                print(f"Processing week {y}-{w}")

                # TODO: Launch processing here (resources retrieval)

                if (getNumberWeeksPerYear(y) == 53 and w == 53) or (getNumberWeeksPerYear(y) == 52 and w == 52):
                    break
                if w == rW[-1] and y == rY[-1]:
                    break
            if not isLooping:
                break

    def getTickData(self, pair: str, yr: Union[str, int], wk: Union[str, int]) -> pd.DataFrame:
        config_: Config = Config(pair, yr, wk, DataType.TICK)
        config_.setUrl()
        q = self._getDataFrame(config=config_)
        q.columns = ["dt", "b", "a"]
        return q

    def getCandleData(self, pair: str, yr: Union[str, int], wk: Union[str, int], fq: str) -> pd.DataFrame:
        config_: Config = Config(pair, yr, wk, DataType.CANDLE, _fq=fq)
        config_.setUrl()
        q = self._getDataFrame(config=config_)
        q.columns = ["dt", *[f"b{sym}" for sym in OHLC], *[f"a{sym}" for sym in OHLC]]
        return q

    # Scraper for 1 week
    # Scraper for a range (start -> end)
    # Scraper with string (YYYY-W to ...)
    # Or scraper for a specific week given a specific day

    def _getDataFrame(self, config: Config) -> pd.DataFrame:
        if not isinstance(config, Config):
            raise Exception("Please enter a valid config.")

        # Constructing the URL
        url: str = config.url
        req = requests.get(url=url, stream=True)
        if req.status_code // 100 != 2:
            raise Exception("Error while requesting data")

        # Downloading .csv.gz (archived file)
        with open(f"{OUT_FOLDER}/{config.getFilename()}.csv.gz", 'wb') as f:
            for chunk in req.raw.stream(1024, decode_content=False):
                if chunk:
                    f.write(chunk)

        # Unzipping .csv.gz into a .csv file (unprocessed CSV)
        with gzip.open(f"{OUT_FOLDER}/{config.getFilename()}.csv.gz", 'rb') as f_in:
            with open(f"{OUT_FOLDER}/{config.getFilename()}.csv", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Reading unprocessed/binary CSV file
        fi = open(f"{OUT_FOLDER}/{config.getFilename()}.csv", 'rb')
        data = fi.read()
        fi.close()

        # Processing + Writing CSV file
        fo = open(f"{OUT_FOLDER}/{config.getFilename()}.csv", 'wb')
        fo.write(data.replace(b'\x00', b''))
        fo.close()

        # Reading CSV file
        df = pd.read_csv(filepath_or_buffer=f"{OUT_FOLDER}/{config.getFilename()}.csv",
                         sep=",",
                         on_bad_lines='skip')
        if self.castDatatime:
            df["DateTime"] = pd.to_datetime(df["DateTime"], format="%m-%d-%Y %H:%M:%S.%f")
        return df
