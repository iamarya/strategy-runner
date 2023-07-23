# exchange quote service
from src.models.enums import INTERVAL_TYPE
from src.models.candle import Candle
from datetime import datetime
from src.exchange.exchange import Exchange, MockExchange


class QuoteService:

    def __init__(self):
        self.exchange: Exchange = MockExchange()

    def get_candles(self, symbol: str, interval: INTERVAL_TYPE, current_time: datetime, no_candles: int) -> list[Candle]:
        from_time = int(current_time.timestamp() -
                        interval.value*(no_candles-1))  # in secs
        to_time = int(current_time.timestamp())
        # check any corner case if it will return 3 candles when expecting 2 candles
        candles = self.exchange.get_candles(
            symbol, interval, from_time, to_time)
        # if len(candles) > no_candles:
        #     candles = candles [-no_candles:]
        return candles
