# exchange quote service
from src.models.enums import Duration
from datetime import datetime
from src.exchange.exchange import Exchange, MockExchange
class QuoteService:

    def __init__(self):
        self.exchange = MockExchange()

    def get_candles(self, symbol:str, duration: Duration, current_time:datetime, no_candles:int):
        # write logic to generate from and to time #todo
        from_time = None
        to_time = None
        candles = self.exchange.get_candles(symbol, duration, from_time, to_time)
        print(candles)


