import pandas as pd

from models.enums import INTERVAL_TYPE

'''
Example:
market_watch = {
    "ETH": {
        "symbol": "ETH",
        M5: DataFrame,
        D1: DataFrame,
        "indicators": [i1, i2], #not added yet, may be not needed
        "ltp": 123.2,
        "last_updated_time": 12222987654,
        "length": 10, # for which df? todo need to update structure or remove this
        "exchange_timezone": UTC #not added yet
    }
}

'''


class MarketWatch:
    def __init__(self) -> None:
        self.data = dict()

    def get_ltp(self, symbol: str) -> float:
        return self.data[symbol].ltp

    def get_candles(self, symbol: str, interval: INTERVAL_TYPE) -> pd.DataFrame:
        return self.data[symbol][interval]

    def get_last_updated(self, symbol: str):
        return self.data[symbol].last_updated_time

    def get_length(self, symbol: str):
        return self.data[symbol].length
