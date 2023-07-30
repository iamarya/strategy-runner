from models.candle import Candle
from models.enums import INTERVAL_TYPE

class Exchange:

    def get_candles(self, symbol: str, inetval: INTERVAL_TYPE, from_time: int, to_time: int) -> list[Candle]:
        # get current running candle and last completed candle
        return []

# python -m strategy_runner.exchange.exchange
# for tesing
