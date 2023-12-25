from .utils import *


class Config:
    __class__: str = "Config"
    __slots__: dict = ("pair", "yr", "wk", "type", "url_", "fq")

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
        if "_fq" in kwargs and kwargs.get("_fq") is not None:
            if str(kwargs["_fq"]) not in Frequency.getAvailableFrequencies():
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
