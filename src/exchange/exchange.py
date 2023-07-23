import random
from src.models.candle import Candle
from src.models.enums import INTERVAL_TYPE
from datetime import datetime
import math


class Exchange:

    def get_candles(self, symbol: str, inetval: INTERVAL_TYPE, from_time: int, to_time: int) -> list[Candle]:
        # get current running candle and last completed candle
        return []


class MockExchange(Exchange):

    def get_candles(self, symbol: str, inetval: INTERVAL_TYPE, from_time: int, to_time: int) -> list[Candle]:
        candles = []
        print("from_time, to_time in secs", from_time, to_time)
        current_candle_time = math.floor(
            from_time/inetval.value) * inetval.value
        while current_candle_time <= to_time:
            candles.append(Candle(current_candle_time,
                           o=random.randint(1, 10), h=random.randint(1, 10), l=random.randint(1, 10), c=random.randint(1, 10), v=100))
            current_candle_time = current_candle_time+inetval.value
        return candles

# python -m strategy_runner.exchange.exchange
# for tesing
