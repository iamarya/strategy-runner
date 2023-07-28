import math
from src.models.candle import Candle
from src.models.enums import INTERVAL_TYPE
from src.engiene.engine_config import EngineConfig, SymbolConfig
import pandas as pd
import numpy as np

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
        "indicators": [i1, i2], #not added yet, may be not needed
        "ltp": 123,
        "last_updated_time": 12222987654,
        "length": 10, # for which df? todo need to update structure or remove this
        "exchange_timezone": UTC #not added yet
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
                # index=range(10) needed if initial size is needed and index to start from 0
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
    
    def add_candles(self, symbol: str, interval: INTERVAL_TYPE, candles: list[Candle]) -> CandleEvent:
        pass

    def add_update_candles(self, symbol: str, interval: INTERVAL_TYPE, candles: list[Candle]) -> CandleEvent:
        df = self.market_watch[symbol][interval]
        candle_event = CandleEvent(symbol, interval, False)
        # too slow for history only, todo add as a single df
        # improvment can be done like add all row at a time
        # somehow also comapring for updated items if needed else just replace everything will be easy
        # current implimentation is comparing row by row
        for candle in candles:
            # last_index = self.market_watch[symbol]["length"]
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
                # self.market_watch[symbol]["length"] = last_index+1
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
        # print(
        #     f"generating candle for {target_interval.name} from {source_interval.name}")
        # print("source_candle_event is", source_candle_event)
        source_df = self.market_watch[symbol][source_interval]
        source_start_index, _ = source_candle_event.get_start_end_time()
        # todo will update formula one time offset is added to exchange
        start_index = math.floor(
            source_start_index/target_interval.value)*target_interval.value
        updated_only_df: pd.DataFrame = source_df.loc[start_index:]
        generated_df: pd.DataFrame = updated_only_df.groupby(np.floor(
            updated_only_df.index/target_interval.value)*target_interval.value).agg(
            open=('open', 'first'),
            high=('high', 'max'),
            low=('low', 'min'),
            close=('close', 'last'),
            volume=('volume', 'sum')
        )
        generated_df.index = generated_df.index.astype('int64')

        candle_event = CandleEvent(symbol, target_interval, True)
        df = self.market_watch[symbol][target_interval]
        for index, row in generated_df.iterrows():
            time: int = index  # type: ignore
            if index in df.index:
                is_updated = False
                # no need to update open
                if df.loc[time, 'high'] < row.high:
                    df.loc[time, 'high'] = row.high
                    is_updated = True
                if df.loc[time, 'low'] > row.low:
                    df.loc[time, 'low'] = row.low
                    is_updated = True
                if df.loc[time, 'close'] != row.close:
                    df.loc[time, 'close'] = row.close
                    is_updated = True
                if df.loc[time, 'volume'] < row.volume:
                    df.loc[time, 'volume'] = row.volume
                    is_updated = True
                # updated
                if is_updated:
                    candle_event.add_to_updated(time)
            else:
                # inserted
                candle_event.add_to_inserted(time)
                df.loc[time, default_columns[1:]] = [
                    row.open, row.high, row.low, row.close, row.volume]

        return candle_event

    '''
    Used for back testing to generate all candle events for history candles
    list[CandleEvent] is for a perticular time for all intervals for single symbol
    list[list[CandleEvent]] is for a perticular time for all intervals for all symbol
    list[list[list[CandleEvent]]] is for a all time for all intervals for all symbol 
    '''

    def synthesized_all_candle_events_all_time(self) -> list[dict[str, list[CandleEvent]]]:
        # get all intervals for history candles

        # getsmallest interval
        return []  # list of list of candle_event

    def get_market_watch(self, symbol: str) -> dict:
        return self.market_watch[symbol]

    def print_market_watch(self, symbol: str) -> None:
        symbol_mw = self.get_market_watch(symbol)
        print(f'\nMarketwatchs for symbol {symbol}')
        for each_int in INTERVAL_TYPE:
            if each_int in symbol_mw:
                print(
                    f"\n[symbol ={symbol}; last_updated_time = {symbol_mw['last_updated_time']}; interval={each_int.name}; ltp = {symbol_mw['ltp']} ]")
                print(symbol_mw[each_int])
