from .constants import *
from typing import Union
import requests
import pandas as pd
import gzip
import shutil
import glob
import os

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
            self.fq = kwargs["_fq"]
            # TODO: Add check on frequency

    def setUrl(self) -> None:
        if self.type == DataType.TICK:
            dom_: str = Url.TICK
            self.url_: str = f"https://{dom_}/{self.pair}/{self.yr}/{self.wk}.{DATA_FILE_EXTENSION}"
        elif self.type == DataType.CANDLE and self.fq is not None:
            dom_: str = Url.CANDLE
            self.url_: str = f"https://{dom_}/{self.fq}/{self.pair}/{self.yr}/{self.wk}.{DATA_FILE_EXTENSION}"

    def getUrl(self) -> str:
        return self.url_

    url = property(fget=getUrl, fset=setUrl)

    def getFilename(self) -> str:
        if self.type == DataType.CANDLE:
            return f"{self.type.value}_{self.pair}_{self.fq}_{self.yr}_{self.wk}"
        return f"{self.type.value}_{self.pair}_{self.yr}_{self.wk}"


class Data:
    # TODO: Init with instrument + check
    # TODO: Scraper and store g-zip into a folder
        # In case of multiple files, lauch multiple threads
    # TODO: Generate a new folder (hex) into /usr/tmp/
    # TODO: Store g-zip and launch a process to unzip each archive
    # Once unzipped, merging
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
            fs = glob.glob("*.csv")
            for f in fs:
                os.remove(f)
        if not self.keepGZIP:
            fs = glob.glob("*.gz")
            for f in fs:
                os.remove(f)

    def __del__(self) -> None:
        self._handleIntemediaryFiles()

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

    # TODO: Add scraper for tick data
    # Parameters: Week + Year
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
        with open(f"{config.getFilename()}.csv.gz", 'wb') as f:
            for chunk in req.raw.stream(1024, decode_content=False):
                if chunk:
                    f.write(chunk)

        # Unzipping .csv.gz into a .csv file (unprocessed CSV)
        with gzip.open(f"{config.getFilename()}.csv.gz", 'rb') as f_in:
            with open(f"{config.getFilename()}.csv", 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        # Reading unprocessed/binary CSV file
        fi = open(f"{config.getFilename()}.csv", 'rb')
        data = fi.read()
        fi.close()

        # Processing + Writing CSV file
        fo = open(f"{config.getFilename()}.csv", 'wb')
        fo.write(data.replace(b'\x00', b''))
        fo.close()

        # Reading CSV file
        df = pd.read_csv(filepath_or_buffer=f"{config.getFilename()}.csv",
                         sep=",",
                         on_bad_lines='skip')
        if self.castDatatime:
            df["DateTime"] = pd.to_datetime(df["DateTime"], format="%m-%d-%Y %H:%M:%S.%f")
        return df
