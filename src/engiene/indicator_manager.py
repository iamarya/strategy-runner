from src.models.candle import Candle
from src.models.market_watch import MarketWatch

class IndicatorManager:
    def __init__(self, market_watch: MarketWatch) -> None:
        self.market_watch: MarketWatch = market_watch

    def create_upadte_indicators(self, candles: list[Candle]):
        # get candles from df and check if candle is exist
        # then update else append the candle 
        # return response (which candles are updated which are created)
        pass