import logging
import math
import random

from exchange.exchange import Exchange
from models.candle import Candle
from models.candle_update_detail import CandleUpdateDetail
from models.enums import INTERVAL_TYPE, EVENT_TYPE, TRANSACTION_TYPE, STATE, ORDER_TYPE
from models.event import Event
from models.record_book import Record
from services.market_watch_service import MarketWatchService
import random

logger = logging.getLogger(__name__)


def generate_id():
    return str(random.randint(10000, 99999))


def get_time_from_candle_event(current_candle_events: list[CandleUpdateDetail]) -> int:
    for event in current_candle_events:
        if event.inserted:
            return event.inserted[-1]


class MockExchange(Exchange):

    def __init__(self):
        self.current_candle_event: dict[str, list[CandleUpdateDetail]] = None
        self.order_book: list[Record] = []

    def is_live(self) -> bool:
        return False

    def set_market_watch_service(self, market_watch_service: MarketWatchService):
        self.market_watch_service = market_watch_service

    def notify(self, event: Event):
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
        # add order to order_book
        curr_time = get_time_from_candle_event(self.current_candle_event.get(symbol))
        curr_price = self.market_watch_service.get_price_from_market_watch_on_candle_event(symbol,
                                                                                           self.current_candle_event)
        rec = Record(order_id, symbol, TRANSACTION_TYPE.BUY, ORDER_TYPE.MARKET, STATE.CONFIRMED, curr_time, curr_time, quantity,
                     price=curr_price)
        self.order_book.append(rec)
        return order_id

    def buy_limit(self, symbol: str, quantity: float, price: float) -> str:
        order_id = generate_id()
        curr_time = get_time_from_candle_event(self.current_candle_event.get(symbol))
        curr_price = self.market_watch_service.get_price_from_market_watch_on_candle_event(symbol,
                                                                                           self.current_candle_event)
        # todo if price is more than market price buy at market price
        rec = Record(order_id, symbol, TRANSACTION_TYPE.BUY, ORDER_TYPE.LIMIT, STATE.PENDING, curr_time, curr_time, quantity,
                     limit_price=price)
        # check if the order is executed inside notify method
        self.order_book.append(rec)
        return order_id

    def buy_market_sl(self, symbol: str, quantity: float, stop_price: float) -> str:
        order_id = generate_id()
        curr_time = get_time_from_candle_event(self.current_candle_event.get(symbol))
        price = self.market_watch_service.get_price_from_market_watch_on_candle_event(symbol, self.current_candle_event)
        rec = Record(order_id, symbol, TRANSACTION_TYPE.BUY, ORDER_TYPE.SL_MARKET, STATE.CONFIRMED, curr_time, curr_time, quantity,
                     price=price, stop_price=stop_price)
        self.order_book.append(rec)
        order_id_sl = generate_id()
        rec_sl = Record(order_id_sl, symbol, TRANSACTION_TYPE.SL, ORDER_TYPE.SL_MARKET, STATE.PENDING, curr_time, curr_time, quantity,
                        stop_price=stop_price, parent_id=order_id)
        # check if the sl is executed inside notify method
        self.order_book.append(rec, rec_sl)
        return order_id

    def buy_limit_sl(self, symbol: str, quantity: float, price: float, stop_price: float) -> str:
        order_id = generate_id()
        curr_time = get_time_from_candle_event(self.current_candle_event.get(symbol))
        curr_price = self.market_watch_service.get_price_from_market_watch_on_candle_event(symbol, self.current_candle_event)
        # todo if price is more than market price buy at market price and add sl order
        rec = Record(order_id, symbol, TRANSACTION_TYPE.BUY, ORDER_TYPE.SL_LIMIT, STATE.PENDING, curr_time, curr_time, quantity,
                     limit_price=price, stop_price=stop_price)
        self.order_book.append(rec)
        return order_id
