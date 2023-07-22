from src.models.candle import Candle
from src.models.enums import INTERVAL_TYPE
from datetime import datetime
import math


class Exchange:

    def get_candles(symbol: str, inetval: INTERVAL_TYPE, from_time: datetime, to_time: datetime) -> list[Candle]:
        # get current running candle and last completed candle
        pass


class MockExchange(Exchange):

    def get_candles(self, symbol: str, inetval: int, from_time: float, to_time: float) -> list[Candle]:
        candles = []
        print("from_time, to_time in secs", from_time, to_time)
        current_candle_time = math.floor(from_time/inetval) * inetval
        while current_candle_time <= to_time:
            candles.append(Candle(current_candle_time,
                           o=6, h=12, l=4, c=8, v=100))
            current_candle_time = current_candle_time+inetval
        return candles

# python -m strategy_runner.exchange.exchange
# for tesing
