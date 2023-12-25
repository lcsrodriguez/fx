from .constants import *
from datetime import *
from typing import Union
import requests
import pandas as pd
import gzip
import shutil
import glob
import os
import threading


def getNumberWeeksPerYear(_yr: int) -> int:
    return int(date(year=_yr, month=12, day=29).isocalendar().week)


def isWeekEnd(dt: Union[date, datetime, str]) -> bool:
    if isinstance(dt, date) or isinstance(dt, datetime):
        return dt.weekday() in [5, 6]
    elif isinstance(dt, str):
        return date.fromisoformat(dt).weekday() in [5, 6]
