from .constants import *
from typing import Union
import requests
import pandas as pd
import gzip
import shutil


class Config:
    __slots__ = ("pair", "yr", "wk", "type", "url_")

    def __init__(self,
                 _pair: str,
                 _yr: Union[str, int],
                 _wk: Union[str, int],
                 _type: str = DataType.TICK) -> None:
        self.pair: str = _pair
        self.yr: Union[str, int] = _yr
        self.wk: Union[str, int] = _wk
        self.type: str = _type
        self.url_: str = ""

    def setUrl(self) -> None:
        if self.type == DataType.TICK:
            dom_: str = Url.TICK
        elif self.type == DataType.CANDLE:
            dom_: str = Url.CANDLE
        self.url_: str = f"https://{dom_}/{self.pair}/{self.yr}/{self.wk}.{DATA_FILE_EXTENSION}"
        print(self.url_)

    def getUrl(self) -> str:
        return self.url_

    url = property(fget=getUrl, fset=setUrl)

    def getFilename(self) -> str:
        return f"{self.pair}_{self.yr}_{self.wk}"


class Data:
    # TODO: Init with instrument + check
    # TODO: Scraper and store g-zip into a folder
        # In case of multiple files, lauch multiple threads
    # TODO: Generate a new folder (hex) into /usr/tmp/
    # TODO: Store g-zip and launch a process to unzip each archive
    # Once unzipped, merging

    @staticmethod
    def getTickData(pair: str, yr: Union[str, int], wk: Union[str, int]):
        config_: Config = Config(pair, yr, wk, DataType.TICK)
        config_.setUrl()
        q = Data._getRequestedArchive(config=config_)
        return q

    @staticmethod
    def getCandleData(pair: str, yr: Union[str, int], wk: Union[str, int]):
        pass


    # TODO: Add scraper for tick data
    # Parameters: Week + Year
    # Scraper for 1 week
    # Scraper for a range (start -> end)
    # Scraper with string (YYYY-W to ...)
    # Or scraper for a specific week given a specific day

    @staticmethod
    def _getRequestedArchive(config: Config) -> pd.DataFrame:
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
        # Uncompressing .csv.gz into a .csv file (unprocessed CSV)
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
        return df