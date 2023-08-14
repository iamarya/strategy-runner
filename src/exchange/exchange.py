from models.candle import Candle
from models.enums import INTERVAL_TYPE


class Exchange:

    def get_candles(self, symbol: str, interval: INTERVAL_TYPE, from_time: int, to_time: int) -> list[Candle]:
        # get current running candle and last completed candle
        return []

    def is_live(self) -> bool:
        pass

    def buy_market(self, symbol: str, quantity: float):
        pass

    def buy_limit(self, symbol: str, quantity: float, price: float):
        pass

    def buy_market_sl(self, symbol: str, quantity: float, stop_price: float):
        pass

    def buy_limit_sl(self, symbol: str, quantity: float, price: float, stop_price: float):
        pass

# python -m strategy_runner.exchange.exchange
# for testing
