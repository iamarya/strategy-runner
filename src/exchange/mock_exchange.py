import logging
import math
import random

from exchange.exchange import Exchange
from models.candle import Candle
from models.candle_update_detail import CandleUpdateDetail
from models.enums import INTERVAL_TYPE, EVENT_TYPE, TRANSACTION_TYPE, STATE, ORDER_TYPE
from models.event import Event
from services.market_watch_service import MarketWatchService

logger = logging.getLogger(__name__)


def generate_id():
    """
    generate the id using the symbol, timeframe, timestamp, so that using order id it
    can be caluated if the order is executed or not.
    """
    return str(random.randint(10000, 99999))


class MockExchange(Exchange):

    def __init__(self):
        self.current_candle_event: dict[str, list[CandleUpdateDetail]]|None = None

    def is_live(self) -> bool:
        return False

    def set_market_watch_service(self, market_watch_service: MarketWatchService):
        self.market_watch_service = market_watch_service

    def get_curr_time_from_candle_event(self, symbol) -> int:
        current_candle_events = self.current_candle_event.get(symbol)
        for event in current_candle_events:
            if event.inserted:
                return event.inserted[-1]

    def notify(self, event: Event):
        """it is used to get current timestamp for order creation and using which it
        can be checked if the order is executed or not.
        """
        if event.type == EVENT_TYPE.CANDLE_EVENT:
            self.current_candle_event = event.value
        else:
            self.current_candle_event = None

    # has properties charge = 1.5, exchange_start_time, end_time, timezone todo

    def get_candles(self, symbol: str, interval: INTERVAL_TYPE, from_time: int, to_time: int) -> list[Candle]:
        candles = []
        logger.debug(
            f"from_time={from_time}, to_time={to_time} in secs for interval={interval.name}")
        current_candle_time = math.floor(
            from_time / interval.value) * interval.value
        while current_candle_time <= to_time:
            candles.append(Candle(current_candle_time,
                                  o=random.randint(1, 10), h=random.randint(1, 10), l=random.randint(1, 10),
                                  c=random.randint(1, 10), v=100))
            current_candle_time = current_candle_time + interval.value
        return candles

    def buy_market(self, symbol: str, quantity: float) -> str:
        order_id = generate_id()
        return order_id

    def buy_limit(self, symbol: str, quantity: float, price: float) -> str:
        order_id = generate_id()
        return order_id

    def buy_market_sl(self, symbol: str, quantity: float, stop_price: float) -> str:
        order_id = generate_id()
        return order_id

    def buy_limit_sl(self, symbol: str, quantity: float, price: float, stop_price: float) -> str:
        order_id = generate_id()
        return order_id
