from exchange.mock_exchange import MockExchange
from exchange.exchange import Exchange


class PositionService:

    def __init__(self):
        self.exchange: Exchange = MockExchange()
