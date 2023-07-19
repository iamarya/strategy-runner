from src.models.candle import Candle
from src.models.enums import INTERVAL_ENUM
from datetime import datetime
import math


class Exchange:

    def get_candles(symbol: str, inetval: INTERVAL_ENUM, from_time: datetime, to_time: datetime) -> list[Candle]:
        # get current running candle and last completed candle
        pass


class MockExchange(Exchange):

    def get_candles(self, symbol: str, inetval: int, from_time: float, to_time: float) -> list[Candle]:
        candles = []
        print(from_time, to_time)
        current_candle_time = round(from_time/inetval) * inetval
        while current_candle_time <= to_time:
            candles.append(Candle(current_candle_time,
                           h=10, l=2, o=4, c=6, v=100))
            current_candle_time = current_candle_time+inetval
        return candles

# python -m strategy_runner.exchange.exchange
# for tesing
