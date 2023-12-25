from typing import List, Dict, Tuple
from datetime import datetime
from enum import Enum

DATA_FILE_EXTENSION: str = "csv.gz"  # G-zip CSV
BASE_URL: str = "fxcorporate.com"
OHLC: list = ["o", "h", "l", "c"]
OUT_FOLDER: str = "out"
TMP_FOLDER: str = "tmp"


class Frequency:
    MINUTE: str = "m1"
    HOUR: str = "H1"
    DAY: str = "D1"

    @staticmethod
    def getAvailableFrequencies() -> list:
        return list([getattr(Frequency, f) for f in Frequency.__annotations__.keys()])


class DataType(Enum):
    TICK: str = "TICK"
    CANDLE: str = "CANDLE"


url: dict = {
    DataType.TICK: f"tickdata.{BASE_URL}",
    DataType.CANDLE: f"candledata.{BASE_URL}"
}


# See limits: https://fxcm-api.readthedocs.io/en/latest/marketdata.html#tickdata
timeRange: dict = {
    DataType.TICK: [str(e) for e in range(2015, datetime.now().year + 1)],
    DataType.CANDLE: [str(e) for e in range(2012, datetime.now().year + 1)]
}


# See list: https://fxcm-api.readthedocs.io/en/latest/marketdata.html#tickdata
AVAILABLE_SYMBOLS: Dict[DataType, List[str]] = {
    DataType.TICK: [
        "AUDCAD", "AUDCHF", "AUDJPY", "AUDNZD", "CADCHF", "EURAUD",
        "EURCHF", "EURGBP", "EURJPY", "EURUSD", "GBPCHF", "GBPJPY",
        "GBPNZD", "GBPUSD", "NZDCAD", "NZDCHF", "NZDJPY", "NZDUSD",
        "USDCAD", "USDCHF", "USDJPY", "AUDUSD", "CADJPY", "GBPCAD",
        "USDTRY", "EURNZD"],
    DataType.CANDLE: [
        "AUDCAD", "AUDCHF", "AUDJPY", "AUDNZD", "CADCHF", "EURAUD",
        "EURCHF", "EURGBP", "EURJPY", "EURUSD", "GBPCHF", "GBPJPY",
        "GBPNZD", "GBPUSD", "NZDCAD", "NZDCHF", "NZDJPY", "NZDUSD",
        "USDCAD", "USDCHF", "USDJPY"]
}

THREADS_POOL_LIMIT: int = 12
