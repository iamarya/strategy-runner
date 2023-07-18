# exchange quote service
from src.models.enums import Duration
import datetime
from src.exchange.exchange import Exchange, MockExchange
class QuoteService:

    def __init__(self):
        self.exchange = MockExchange()

    def get_currect_candle(self, symbol:str, duration: Duration, time:datetime.datetime):
        candles = self.exchange.get_current_candles(symbol, duration)
        print(candles)


