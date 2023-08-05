from models.candle import Candle
from config.engine_config import SymbolConfig
from models.candle_update_detail import CandleUpdateDetail
from indicators.indicator import Indicator
from services.market_watch_service import MarketWatchService


class IndicatorManager:
    def __init__(self, market_watch_serice: MarketWatchService) -> None:
        self.market_watch_serice = market_watch_serice

    def create_upadte_indicators(self, candle_update_detail: CandleUpdateDetail, indicator: Indicator):
        if not candle_update_detail.updated and not candle_update_detail.inserted:
            print("no change in candles", candle_update_detail)
            return
        df = self.market_watch_serice.get_candles(
            candle_update_detail.symbol, candle_update_detail.interval)
        start_index, end_index = candle_update_detail.get_start_end_time()
        # position is needed to calculate indicators easily
        start_position = df.index.get_loc(start_index)
        end_position = df.index.get_loc(end_index)
        indicator.process(self.market_watch_serice.get_candles(
            candle_update_detail.symbol, candle_update_detail.interval), start_position, end_position)
