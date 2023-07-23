from src.engiene.engine_config import SymbolConfig
from src.models.candle import Candle
from src.models.event import CandleEvent
from src.models.market_watch import MarketWatch
from src.models.enums import INTERVAL_TYPE


class CandleManager:
    def __init__(self, market_watch: MarketWatch) -> None:
        self.market_watch: MarketWatch = market_watch

    def create_upadte_candles(self, interval:INTERVAL_TYPE, candles: list[Candle], symbol: str) -> CandleEvent:
        # get candles from df and check if candle is exist
        # then update else append the candle
        # return response (which candles are updated which are created)
        return self.market_watch.add_update_candles(symbol, interval,
                                                    candles)
    def generate_candles(self):
        pass
    
    def synthesize_all_candle_events(self) -> list:
        return []