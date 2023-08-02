from binance.client import Client
from dotenv import load_dotenv
import os

from models.candle import Candle
from models.enums import INTERVAL_TYPE
from exchange.exchange import Exchange
from pyrate_limiter import Duration, RequestRate, Limiter

load_dotenv()
_client = Client(os.getenv('BINANCE_API_KEY'), os.getenv('BINANCE_API_SECRET'))

request_weight_rate = RequestRate(1200, Duration.MINUTE)
request_weight_rate = Limiter(request_weight_rate)

class Bianace(Exchange):

    @request_weight_rate.ratelimit('identity', delay=True, max_delay=360)
    def get_candles(self, symbol: str, interval: INTERVAL_TYPE, from_time: int, to_time: int) -> list[Candle]:
        # todo calculates windows max of 1000 candles between from and to and join them, take care of ratelimit also
        sourec_candles = _client.get_klines(
            symbol=symbol, interval=_get_interval(interval), limit=1000)
        return [Candle(i[0], i[1], i[2], i[3], i[4], i[5]) for i in sourec_candles]


def _get_interval(from_interval: INTERVAL_TYPE) -> str:
    if from_interval == INTERVAL_TYPE.M15:
        return Client.KLINE_INTERVAL_15MINUTE
    return ""


if __name__ == '__main__':
    b = Bianace()
    print(len(b.get_candles('BTCUSDT', INTERVAL_TYPE.M15, 1, 1))) # type: ignore
