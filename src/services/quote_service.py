# exchange quote service
import math
from models.enums import INTERVAL_TYPE
from models.candle import Candle
from datetime import datetime
from exchange.exchange import Exchange


class QuoteService:

    def get_candles(self, exchange: Exchange, symbol: str, interval: INTERVAL_TYPE, current_time: datetime,
                    no_candles: int) -> list[Candle]:
        from_time = int(current_time.timestamp() -
                        interval.value*(no_candles-1))  # in secs
        # convert from_time to base of candle start time
        from_time = math.floor(
            from_time / interval.value) * interval.value
        to_time = int(current_time.timestamp())
        candles = exchange.get_candles(
            symbol, interval, from_time, to_time)
        # check any corner case if it will return 3 candles when expecting 2 candles
        # should not happen, even if comes it will check and update without issue
        # if len(candles) > no_candles:
        #     candles = candles [-no_candles:]
        # print("candles received for above inputs:", candles)
        return candles
