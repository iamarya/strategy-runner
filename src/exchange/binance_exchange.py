import datetime
import math
from binance.client import Client
from dotenv import load_dotenv
import os

from models.candle import Candle
from models.enums import INTERVAL_TYPE, MODE
from exchange.exchange import Exchange
from pyrate_limiter import Duration, RequestRate, Limiter
import logging

logger = logging.getLogger(__name__)
load_dotenv()

MAX_CANDLES = 1000

request_weight_rate = RequestRate(1200, Duration.MINUTE)
request_weight_limiter = Limiter(request_weight_rate)


class BinanceExchange(Exchange):

    def __init__(self, mode: MODE) -> None:
        super().__init__()
        self._mode = mode
        if self._mode == MODE.LIVE:
            logger.warning("BinanceExchange is LIVE mode")
            self._client = Client(
                os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_API_SECRET'))
        elif self._mode == MODE.SANDBOX:
            logger.warning("BinanceExchange is SANDBOX mode")
            self._client = Client(os.getenv('TEST_BINANCE_API_KEY'), os.getenv(
                'TEST_BINANCE_API_SECRET'), testnet=True)
        else:
            logger.error("BinanceExchange client not initiated as no mode is configured.")

    def is_live(self) -> bool:
        return self._mode == MODE.LIVE

    def get_candles(self, symbol: str, interval: INTERVAL_TYPE, from_time: int, to_time: int) -> list[Candle]:
        interval_binance = self._get_interval(interval)
        start = from_time
        end = start + interval.value*(MAX_CANDLES-1)
        candles: list[Candle] = []
        while start < to_time:
            candles.extend(self._get_candles_request(
                symbol, interval_binance, start, end))  # type: ignore
            start = start + interval.value * MAX_CANDLES
            end = start + interval.value*(MAX_CANDLES-1)
            if end > to_time:
                end = to_time
        return candles

    @request_weight_limiter.ratelimit('get_candles', delay=True, max_delay=360)
    def _get_candles_request(self, symbol: str, interval_binance: str, from_time: int, to_time: int) -> list[Candle]:
        logger.debug(f'from_time: {from_time}, to_time:{to_time}')
        source_candles = self._client.get_klines(
            symbol=symbol, interval=interval_binance, startTime=from_time*1000, endTime=to_time*1000, limit=MAX_CANDLES)
        candles = [Candle(math.floor(i[0]/1000), float(i[1]), float(i[2]),
                          float(i[3]), float(i[4]), float(i[5])) for i in source_candles]
        # print(candles)
        return candles

    @staticmethod
    def _get_interval(from_interval: INTERVAL_TYPE) -> str:
        if from_interval == INTERVAL_TYPE.M5:
            return Client.KLINE_INTERVAL_5MINUTE
        elif from_interval == INTERVAL_TYPE.M15:
            return Client.KLINE_INTERVAL_15MINUTE
        elif from_interval == INTERVAL_TYPE.HR1:
            return Client.KLINE_INTERVAL_1HOUR
        elif from_interval == INTERVAL_TYPE.D1:
            return Client.KLINE_INTERVAL_1DAY
        elif from_interval == INTERVAL_TYPE.W1:
            return Client.KLINE_INTERVAL_1WEEK

        raise TypeError("binance does not have INTERVAL_TYPE", from_interval)


if __name__ == '__main__':
    b = BinanceExchange(MODE.LIVE)
    current_time = datetime.datetime.now()
    interval = INTERVAL_TYPE.M15
    no_candles = 3
    from_time = int(current_time.timestamp() -
                    interval.value*(no_candles-1))  # in secs
    from_time = math.floor(
        from_time / interval.value) * interval.value
    to_time = int(current_time.timestamp())
    logger.debug(f'from_time: {from_time}, to_time:{to_time}')
    logger.debug(b.get_candles('BTCUSDT', INTERVAL_TYPE.M15, from_time, to_time))
