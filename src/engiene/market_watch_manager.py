import math
import os
from models.candle import Candle
from models.enums import INTERVAL_TYPE
from models.engine_config import SymbolsConfig
import pandas as pd
import numpy as np

from models.candle_update_detail import CandleUpdateDetail
from services.market_watch_service import MarketWatchService

default_columns = ['time', 'open', 'high', 'low', 'close', 'volume']

pd.options.mode.copy_on_write = False


# todo move logics to market_watch_service and a MarketWatch class
class MarketWatchManager:

    def __init__(self, symbols_configs: list[SymbolsConfig], market_watch_service: MarketWatchService) -> None:
        self.market_watch_service = market_watch_service
        # setup initial ma using config
        for symbols_config in symbols_configs:
            for symbol in symbols_config.symbols:
                config = symbols_config.symbol_config
                mw_item = dict()
                # index=range(10) needed if initial size is needed and index to start from 0
                indicator_columns = []
                for indicator in config.indicators():
                    indicator_columns.extend(indicator.get_columns())
                all_columns = default_columns + indicator_columns
                for interval in config.history_intervals() + config.current_intervals() + \
                        config.history_intervals_generated() + config.current_intervals_generated():
                    df = pd.DataFrame(columns=all_columns)
                    df.set_index("time", inplace=True)
                    mw_item[interval] = df
                mw_item["length"] = 0
                mw_item["last_updated_time"] = None
                mw_item["symbol"] = symbol
                self.market_watch_service.market_watch[symbol] = mw_item

    def add_update_candles(self, symbol: str, interval: INTERVAL_TYPE, candles: list[Candle]) -> CandleUpdateDetail:
        df = self.market_watch_service.market_watch[symbol][interval]
        candle_update_detail = CandleUpdateDetail(symbol, interval, False)
        for candle in candles:
            # last_index = self.market_watch_service.market_watch[symbol]["length"]
            wo_time = [candle.o, candle.h, candle.l, candle.c, candle.v]
            if candle.t in df.index:
                if df.loc[candle.t, default_columns[1:]].values.flatten().tolist() != wo_time:
                    # updated
                    candle_update_detail.add_to_updated(candle.t)
                    df.loc[candle.t, default_columns[1:]] = wo_time
            else:
                # inserted
                candle_update_detail.add_to_inserted(candle.t)
                df.loc[candle.t, default_columns[1:]] = wo_time
                # self.market_watch_service.market_watch[symbol]["length"] = last_index+1
        last_updated_time = self.market_watch_service.market_watch[symbol]["last_updated_time"]
        if last_updated_time is None or last_updated_time < candles[-1].t:
            self.market_watch_service.market_watch[symbol]["last_updated_time"] = candles[-1].t
        self.market_watch_service.market_watch[symbol]["ltp"] = candles[-1].c
        # print(self.market_watch_service.market_watch[symbol])
        # print("candle_update_detail", candle_update_detail)
        return candle_update_detail

    def add_candles(self, symbol: str, interval: INTERVAL_TYPE, candles: list[Candle]) -> CandleUpdateDetail:
        df: pd.DataFrame = self.market_watch_service.market_watch[symbol][interval]
        # create a new index series from candles
        add_df = pd.DataFrame([[c.t, c.o, c.h, c.l, c.c, c.v] for c in candles], columns=default_columns)
        add_df.set_index("time", inplace=True)
        add_df.index = add_df.index.astype('int64')

        df = pd.concat([df, add_df])
        candle_update_detail = CandleUpdateDetail(symbol, interval, False)
        candle_update_detail.add_to_inserted_as_list(df.index.to_list())
        self.market_watch_service.market_watch[symbol][interval] = df
        last_updated_time = self.market_watch_service.market_watch[symbol]["last_updated_time"]
        if last_updated_time is None or last_updated_time < candles[-1].t:
            self.market_watch_service.market_watch[symbol]["last_updated_time"] = candles[-1].t
        self.market_watch_service.market_watch[symbol]["ltp"] = candles[-1].c
        return candle_update_detail

    '''DOUBT : candle timestamp should be future or past/ completed candle????? clear: its always past. basically 
    starting sec of the period. ex today is 24th the starting sec of 24th for day candle.'''

    def generate_candles(self, symbol: str, source_interval: INTERVAL_TYPE,
                         source_candle_update_detail: CandleUpdateDetail, target_interval: INTERVAL_TYPE):
        # print(
        #     f"generating candle for {target_interval.name} from {source_interval.name}")
        # print("source_candle_update_detail is", source_candle_update_detail)
        source_df = self.market_watch_service.market_watch[symbol][source_interval]
        source_start_index, _ = source_candle_update_detail.get_start_end_time()
        # todo will update formula one time offset is added to exchange
        start_index = math.floor(
            source_start_index / target_interval.value) * target_interval.value
        updated_only_df: pd.DataFrame = source_df.loc[start_index:]
        generated_df: pd.DataFrame = updated_only_df.groupby(by=np.floor(
            updated_only_df.index / target_interval.value) * target_interval.value).agg(
            open=('open', 'first'),
            high=('high', 'max'),
            low=('low', 'min'),
            close=('close', 'last'),
            volume=('volume', 'sum')
        )
        generated_df.index = generated_df.index.astype('int64')

        candle_update_detail = CandleUpdateDetail(symbol, target_interval, True)
        df = self.market_watch_service.market_watch[symbol][target_interval]
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
                    candle_update_detail.add_to_updated(time)
            else:
                # inserted
                candle_update_detail.add_to_inserted(time)
                df.loc[time, default_columns[1:]] = [
                    row.open, row.high, row.low, row.close, row.volume]

        return candle_update_detail

    '''
    Used for back testing to generate all candle update details for history candles
    list[CandleUpdateDetail] is for a particular time, particular symbol for all intervals
    dict[str, list[CandleUpdateDetail]] is for a particular time of above
    list[dict[str, list[CandleUpdateDetail]]] is for all time of above
    '''

    def synthesized_all_candle_update_details_all_time(self) -> list[dict[str, list[CandleUpdateDetail]]]:
        all_times = pd.Series()
        # get all intervals for history candles
        for item in self.market_watch_service.market_watch.values():
            for key in item.keys():
                if type(key) == INTERVAL_TYPE:
                    df: pd.DataFrame = item[key]
                    all_times = pd.concat([all_times, df.index.to_series()])
        all_times = all_times.drop_duplicates()
        all_times = all_times.sort_index().to_list()

        all_candle_update_details_all_time: list[dict[str, list[CandleUpdateDetail]]] = []

        for time in all_times:
            symbol_dict = {}
            for item in self.market_watch_service.market_watch.values():
                # for each symbol
                symbol = item['symbol']
                candles_for_symbol = []
                for key in item.keys():
                    if type(key) == INTERVAL_TYPE:
                        df: pd.DataFrame = item[key]
                        try:
                            _ = df.loc[time]
                            ce = CandleUpdateDetail(symbol, key, False)
                            ce.add_to_inserted(time)
                            candles_for_symbol.append(ce)
                        except KeyError:
                            pass
                symbol_dict[symbol] = candles_for_symbol
            all_candle_update_details_all_time.append(symbol_dict)
            # print(all_candle_update_details_all_time)
        return all_candle_update_details_all_time

    def save_candles_csv(self):
        # csv per symbol, per interval 
        if not os.path.exists('../tmp'):
            os.makedirs('../tmp')
        for item in self.market_watch_service.market_watch.values():
            symbol = item['symbol']
            for key in item.keys():
                if type(key) == INTERVAL_TYPE:
                    filename = f'../tmp/{symbol}_{key.name}.csv'
                    item[key].to_csv(filename, sep=',', encoding='utf-8', header='true')

    def get_market_watch(self, symbol: str) -> dict:
        return self.market_watch_service.market_watch[symbol]

    def print_market_watch(self, symbol: str) -> None:
        symbol_mw = self.get_market_watch(symbol)
        print(f'\nMarket watches for symbol {symbol}')
        for each_int in INTERVAL_TYPE:
            if each_int in symbol_mw:
                print(
                    f"\n[symbol ={symbol}; last_updated_time = {symbol_mw['last_updated_time']};"
                    f" interval={each_int.name}; ltp = {symbol_mw['ltp']} ]")
                print(symbol_mw[each_int])
