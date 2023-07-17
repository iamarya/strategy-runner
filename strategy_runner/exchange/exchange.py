from strategy_runner.models.candle import Candle
from strategy_runner.models.enums import Duration
from time import time


class Exchange:

    def getHistoryCandles(symbol: str, duration: Duration, from_time: time, to_time: time) -> list[Candle]:
        # get history candles inclusing from_time and to_time
        pass

    def getCurrentCandles(symbol: str, duration: Duration) -> list[Candle]:
        # get current running candle and last completed candle
        pass


class MockExchange(Exchange):
    def getHistoryCandles(symbol: str, duration: Duration, from_time: time, to_time: time) -> list[Candle]:
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