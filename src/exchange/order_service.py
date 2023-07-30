# exchange quote service
from models.enums import INTERVAL_TYPE
from models.candle import Candle
from datetime import datetime
from exchange.exchange import Exchange, MockExchange


class OrderService:

    def __init__(self):
        self.exchange: Exchange = MockExchange()
