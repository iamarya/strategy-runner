from src.models.candle import Candle
from src.models.enums import INTERVAL_TYPE
from src.engiene.engine_config import EngineConfig, SymbolConfig
import pandas as pd

from src.models.event import CandleEvent

default_columns = ['time', 'open', 'high', 'low', 'close', 'volume']

pd.options.mode.copy_on_write = False


class MarketWatch:

    def __init__(self, configs: EngineConfig) -> None:
        self.ma = dict()
        # setup initial ma using config
        for config in configs.get_all_configs():
            mw_item = dict()
            # , index=range(10) needed if initial size
            indicator_coulmns = []
            for indicator in config.indicators():
                indicator_coulmns.extend(indicator.get_columns())
            all_columns = default_columns+indicator_coulmns
            for interval in config.history_intervals() + config.current_intervals() \
                    + config.history_intervals_generated() + config.current_intervals_generated():
                df = pd.DataFrame(columns=all_columns)
                df.set_index("time", inplace=True)
                mw_item[interval] = df
            mw_item["length"] = 0
            mw_item["last_updated_time"] = None
            self.ma[config.symbol()] = mw_item

    def get_ltp(self, symbol: str) -> float:
        return self.ma[symbol].ltp

    def get_candles(self, symbol: str, interval: INTERVAL_TYPE) -> pd.DataFrame:
        return self.ma[symbol][interval]

    def get_last_updated(self, symbol: str):
        return self.ma[symbol].last_updated_time

    def get_length(self, symbol: str):
        return self.ma[symbol].length

    def add_update_candles(self, symbol: str, interval: INTERVAL_TYPE, candles: list[Candle]) -> CandleEvent:
        # improvment can be done like add all row at a time
        # somehow also comapring for updated items if needed else just replace everything will be easy
        # current implimentation is comparing row by row
        df = self.ma[symbol][interval]
        candle_event = CandleEvent(symbol, interval)
        for candle in candles:
            last_index = self.ma[symbol]["length"]
            wo_time = [candle.o, candle.h, candle.l, candle.c, candle.v]
            if candle.t in df.index:
                if df.loc[candle.t, default_columns[1:]].values.flatten().tolist() != wo_time:
                    # updated
                    candle_event.add_to_updated(candle.t)
                    df.loc[candle.t, default_columns[1:]] = wo_time
            else:
                # inserted
                candle_event.add_to_inserted(candle.t)
                df.loc[candle.t, default_columns[1:]] = wo_time
                self.ma[symbol]["length"] = last_index+1
        self.ma[symbol]["last_updated_time"] = candles[-1].t
        self.ma[symbol]["ltp"] = candles[-1].c
        # print(self.ma)
        # print("candle_event", candle_event)
        return candle_event


'''
Example:
{
    "ETH": {
        "symbol": "ETH", # not added yet
        M5: None: DataFrame,
        D1: None,
        "indicators": [i1, i2], #may be not needed
        "ltp": 123,
        "last_updated_time": 12222987654
        "length": 10 # commented
    }
}

'''
