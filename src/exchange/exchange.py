from src.models.candle import Candle
from src.models.enums import Duration
from datetime import datetime


class Exchange:

    def getHistoryCandles(symbol: str, duration: Duration, from_time: datetime, to_time: datetime) -> list[Candle]:
        # get history candles inclusing from_time and to_time
        pass

    def getCurrentCandles(symbol: str, duration: Duration) -> list[Candle]:
        # get current running candle and last completed candle
        pass


class MockExchange(Exchange):

    def getHistoryCandles(symbol: str, duration: Duration, from_time: datetime, to_time: datetime) -> list[Candle]:
        candles = []
        candle_time = from_time
        while candle_time <= to_time:
            candles.append(Candle(h=10, t=candle_time, l=2, o=4, c=6))
            candle_time = candle_time + duration.value
        return candles

    def getCurrentCandles(symbol: str, duration: Duration) -> list[Candle]:
        candles = []
        candles.append(Candle(h=10, l=2, o=4, c=6))
        candles.append(Candle(h=10, l=2, o=4, c=6))
        return candles

# python -m strategy_runner.exchange.exchange
# for tesing
