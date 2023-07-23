from src.models.candle import Candle
from src.models.market_watch import MarketWatch
from src.engiene.engine_config import SymbolConfig
from src.models.event import CandleEvent
from src.indicators.indicator import Indicator


class IndicatorManager:
    def __init__(self, market_watch: MarketWatch) -> None:
        self.mw = market_watch

    def create_upadte_indicators(self, candle_event: CandleEvent, indicator: Indicator):
        if not candle_event.updated and not candle_event.inserted:
            print("no change in candles")
            return
        df = self.mw.get_candles(candle_event.symbol, candle_event.interval)
        start_index = df.index.get_loc(
            candle_event.updated[0]) if candle_event.updated else df.index.get_loc(candle_event.inserted[0])
        end_index = df.index.get_loc(
            candle_event.inserted[-1]) if candle_event.inserted else df.index.get_loc(candle_event.updated[-1])
        indicator.process(self.mw.get_candles(
            candle_event.symbol, candle_event.interval), start_index, end_index)
