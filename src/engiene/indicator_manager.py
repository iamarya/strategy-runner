from models.candle import Candle
from engiene.market_watch_manager import MarketWatchManager
from config.engine_config import SymbolConfig
from models.event import CandleEvent
from indicators.indicator import Indicator


class IndicatorManager:
    def __init__(self, market_watch_manager: MarketWatchManager) -> None:
        self.market_watch_manager = market_watch_manager

    def create_upadte_indicators(self, candle_event: CandleEvent, indicator: Indicator):
        if not candle_event.updated and not candle_event.inserted:
            print("no change in candles", candle_event)
            return
        df = self.market_watch_manager.get_candles(
            candle_event.symbol, candle_event.interval)
        start_index, end_index = candle_event.get_start_end_time()
        # position is needed to calculate indicators easily
        start_position = df.index.get_loc(start_index)
        end_position = df.index.get_loc(end_index)
        indicator.process(self.market_watch_manager.get_candles(
            candle_event.symbol, candle_event.interval), start_position, end_position)
