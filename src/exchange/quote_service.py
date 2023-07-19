# exchange quote service
from src.models.enums import Duration
from datetime import datetime
from src.exchange.exchange import Exchange, MockExchange
class QuoteService:

    def __init__(self):
        self.exchange = MockExchange()

    def get_candles(self, symbol:str, duration: Duration, current_time:datetime, no_candles:int):
        from_time = current_time.timestamp() - duration.value["secs"] * no_candles
        to_time = current_time.timestamp()
        candles = self.exchange.get_candles(symbol, duration, from_time, to_time)
        print(candles)


