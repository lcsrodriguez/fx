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
        pass

    @staticmethod
    def getCandleData(pair: str, yr: Union[str, int], wk: Union[str, int]):
        pass

    @staticmethod
    def getData(ins: str, yr: Union[str, int], wk: Union[str, int]):
        url: str = f"https://{URL.TICK}/{ins}/{yr}/{wk}.{DATA_FILE_EXTENSION}"
        return a(url)

    # TODO: Add scraper for tick data
    # Parameters: Week + Year
    # Scraper for 1 week
    # Scraper for a range (start -> end)
    # Scraper with string (YYYY-W to ...)
    # Or scraper for a specific week given a specific day

    @staticmethod
    def a(url: str = "") -> pd.DataFrame:
        if not isinstance(url, str) or len(url) <= 10:
            raise Exception("Please enter a valid URL.")

        req = requests.get(url)
        if req.status_code//100 != 2:
            raise Exception("Error while requesting data")
        return req.status_code