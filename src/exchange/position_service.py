# exchange quote service
from src.models.enums import INTERVAL_TYPE
from src.models.candle import Candle
from datetime import datetime
from src.exchange.exchange import Exchange, MockExchange


class PositionService:

    def __init__(self):
        self.exchange:Exchange = MockExchange()

    


 