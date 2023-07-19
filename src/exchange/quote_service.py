# exchange quote service
from src.models.enums import INTERVAL_ENUM
from datetime import datetime
from src.exchange.exchange import Exchange, MockExchange
class QuoteService:

    def __init__(self):
        self.exchange:Exchange = MockExchange()

    def get_candles(self, symbol:str, interval: INTERVAL_ENUM, current_time:datetime, no_candles:int):
        from_time = current_time.timestamp() - interval.value.secs * no_candles
        to_time = current_time.timestamp()
        # check any corner case if it will return 3 candles when expecting 2 candles
        candles = self.exchange.get_candles(symbol, interval.value.secs, from_time, to_time)
        print(candles)


