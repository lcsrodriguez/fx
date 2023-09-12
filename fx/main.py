from .constants import *
from typing import Union
from abc import ABC, abstractmethod
import requests
import pandas as pd


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
        pass

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

        url: str = config.url
        req = requests.get(url=url, stream=True)
        if req.status_code // 100 != 2:
            raise Exception("Error while requesting data")

        req.raw.decode_content = True
        f_in = gzip.GzipFile(fileobj=req.raw)
        with open(f"{config.pair}_{config.yr}_{config.wk}.csv", 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
        a = f_in.read()
        return req.status_code