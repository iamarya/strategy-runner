import logging
import math
import random

from exchange.exchange import Exchange
from models.candle import Candle
from models.enums import INTERVAL_TYPE

logger = logging.getLogger(__name__)


class MockExchange(Exchange):

    def is_live(self) -> bool:
        return False

    # has propoties charge = 1.5, exchange_start_time, end_time, timezone todo

    def get_candles(self, symbol: str, inetval: INTERVAL_TYPE, from_time: int, to_time: int) -> list[Candle]:
        candles = []
        logger.debug(
            f"from_time={from_time}, to_time={to_time} in secs for interval={inetval.name}")
        current_candle_time = math.floor(
            from_time / inetval.value) * inetval.value
        while current_candle_time <= to_time:
            candles.append(Candle(current_candle_time,
                                  o=random.randint(1, 10), h=random.randint(1, 10), l=random.randint(1, 10),
                                  c=random.randint(1, 10), v=100))
            current_candle_time = current_candle_time + inetval.value
        return candles
