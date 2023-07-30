from .constants import *

from abc import ABC, abstractmethod
import requests
import fxcmpy
import pandas as pd


class Data(ABC):
    def _getData(self) -> pd.DataFrame:
        pass


class TickData:
    def __init__(self) -> None:
        raise NotImplementedError


class CandleData:
    def __init__(self) -> None:
        raise NotImplementedError
