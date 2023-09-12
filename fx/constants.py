from typing import List, Generator, Iterable
from datetime import datetime
from enum import Enum

DATA_FILE_EXTENSION: str = "csv.gz"  # G-zip CSV
BASE_URL: str = "fxcorporate.com"

# See list: https://fxcm-api.readthedocs.io/en/latest/marketdata.html#tickdata
AVAILABLE_SYMBOLS: List[str] = [
    "AUDCAD", "AUDCHF", "AUDJPY", "AUDNZD", "CADCHF", "EURAUD",
    "EURCHF", "EURGBP", "EURJPY", "EURUSD", "GBPCHF", "GBPJPY",
    "GBPNZD", "GBPUSD", "NZDCAD", "NZDCHF", "NZDJPY", "NZDUSD",
    "USDCAD", "USDCHF", "USDJPY", "AUDUSD", "CADJPY", "GBPCAD",
    "USDTRY", "EURNZD"
]


class DataType(Enum):
    TICK: int = 0
    CANDLE: int = 1


class Url:
    TICK: str = f"tickdata.{BASE_URL}"
    CANDLE: str = f"candledata.{BASE_URL}"


# See limits: https://fxcm-api.readthedocs.io/en/latest/marketdata.html#tickdata
class TimeRange:
    TICK: List[str] = [str(e) for e in range(2015, datetime.now().year + 1)]
    CANDLE: List[str] = [str(e) for e in range(2012, datetime.now().year + 1)]

