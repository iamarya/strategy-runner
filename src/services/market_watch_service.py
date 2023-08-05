
import pandas as pd
from models.enums import INTERVAL_TYPE
from models.market_watch import MarketWatch


class MarketWatchService:
    def __init__(self) -> None:
        self.market_watch = dict()

    def get_ltp(self, symbol: str) -> float:
        return self.market_watch[symbol].ltp

    def get_candles(self, symbol: str, interval: INTERVAL_TYPE) -> pd.DataFrame:
        return self.market_watch[symbol][interval]

    def get_last_updated(self, symbol: str):
        return self.market_watch[symbol].last_updated_time

    def get_length(self, symbol: str):
        return self.market_watch[symbol].length