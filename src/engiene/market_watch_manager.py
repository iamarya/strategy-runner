from src.models.candle import Candle
from src.models.enums import INTERVAL_TYPE
from src.engiene.engine_config import EngineConfig, SymbolConfig
import pandas as pd

from src.models.event import CandleEvent

default_columns = ['time', 'open', 'high', 'low', 'close', 'volume']

pd.options.mode.copy_on_write = False

'''
Example:
market_watch = {
    "ETH": {
        "symbol": "ETH",
        M5: DataFrame,
        D1: DataFrame,
        "indicators": [i1, i2], #may be not needed
        "ltp": 123,
        "last_updated_time": 12222987654
        "length": 10 
    }
}

'''


class MarketWatchManager:

    def __init__(self, engine_config: EngineConfig) -> None:
        self.market_watch = dict()
        # setup initial ma using config
        for symbols_config in engine_config.get_all_configs():
            for symbol in symbols_config.symbols:
                config = symbols_config.symbol_config
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
                mw_item["symbol"] = symbol
                self.market_watch[symbol] = mw_item

    def get_ltp(self, symbol: str) -> float:
        return self.market_watch[symbol].ltp

    def get_candles(self, symbol: str, interval: INTERVAL_TYPE) -> pd.DataFrame:
        return self.market_watch[symbol][interval]

    def get_last_updated(self, symbol: str):
        return self.market_watch[symbol].last_updated_time

    def get_length(self, symbol: str):
        return self.market_watch[symbol].length

    def add_update_candles(self, symbol: str, interval: INTERVAL_TYPE, candles: list[Candle]) -> CandleEvent:
        # improvment can be done like add all row at a time
        # somehow also comapring for updated items if needed else just replace everything will be easy
        # current implimentation is comparing row by row
        df = self.market_watch[symbol][interval]
        candle_event = CandleEvent(symbol, interval)
        for candle in candles:
            last_index = self.market_watch[symbol]["length"]
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
                self.market_watch[symbol]["length"] = last_index+1
        last_updated_time = self.market_watch[symbol]["last_updated_time"]
        if last_updated_time == None or last_updated_time < candles[-1].t:
            self.market_watch[symbol]["last_updated_time"] = candles[-1].t
        self.market_watch[symbol]["ltp"] = candles[-1].c
        # print(self.market_watch[symbol])
        # print("candle_event", candle_event)
        return candle_event

    '''
    DOUBT : candle timestamp should be future or past/ completed candle?????
    clear: its always past. basically starting sec of the period. ex today is 24th the starting sec of 24th for day candle.
    '''

    def generate_candles(self, symbol: str, source_interval: INTERVAL_TYPE,
                         source_candle_event: CandleEvent, target_interval: INTERVAL_TYPE):
        df = self.market_watch[symbol][target_interval]
        candle_event = CandleEvent(symbol, target_interval)

        # todo generate, dont think much, use loop like above for each candle to inster
        # and updated as this is not needed for history/backtest mainly
        return candle_event

    '''
    Used for back testing to generate all candle events for history candles
    list[CandleEvent] is for a perticular time for all intervals for single symbol
    list[list[CandleEvent]] is for a perticular time for all intervals for all symbol
    list[list[list[CandleEvent]]] is for a all time for all intervals for all symbol 
    '''

    def synthesized_all_candle_events_all_time(self) -> list[list[list[CandleEvent]]]:
        # get all intervals for history candles

        # getsmallest interval
        return []  # list of list of candle_event
