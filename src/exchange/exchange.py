from src.models.candle import Candle
from src.models.enums import Duration
from datetime import datetime


class Exchange:

    def get_candles(symbol: str, duration: Duration, from_time:datetime, to_time:datetime) -> list[Candle]:
        # get current running candle and last completed candle
        pass


class MockExchange(Exchange):

    def get_candles(self, symbol: str, duration: Duration, from_time:datetime, to_time:datetime) -> list[Candle]:
        candles = []
        print(from_time, to_time)
        candles.append(Candle(None, h=10, l=2, o=4, c=6, v=100))
        candles.append(Candle(None, h=10, l=2, o=4, c=6, v=100))
        return candles

# python -m strategy_runner.exchange.exchange
# for tesing
