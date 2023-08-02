DATA_FILE_EXTENSION: str = "csv.gz" # G-zip CSV

AVAILABLE_SYMBOLS: list = [
    "AUDCAD", "AUDCHF", "AUDJPY", "AUDNZD", "CADCHF", "EURAUD",
    "EURCHF", "EURGBP", "EURJPY", "EURUSD", "GBPCHF", "GBPJPY",
    "GBPNZD", "GBPUSD", "NZDCAD", "NZDCHF", "NZDJPY", "NZDUSD",
    "USDCAD", "USDCHF", "USDJPY", "AUDUSD", "CADJPY", "GBPCAD",
    "USDTRY", "EURNZD"
]

BASE_URL: str = "fxcorporate.com"

class Subdomain:
    TICK: str = "tickdata"
    CANDLE: str = "candledata"
    OHLC: str = "candledata"
