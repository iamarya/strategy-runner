from exchange.mock_exchange import MockExchange
from exchange.exchange import Exchange


class OrderService:

    def __init__(self):
        self.exchange: Exchange = MockExchange()
