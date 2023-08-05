# exchange quote service
from exchange.mock_exchange import MockExchange
from models.enums import INTERVAL_TYPE
from models.candle import Candle
from datetime import datetime
from exchange.exchange import Exchange


class OrderService:

    def __init__(self):
        self.exchange: Exchange = MockExchange()
