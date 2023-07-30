

from db.db import Db
from exchange.exchange import Exchange
from models.event import CandleEvent


class Strategy:

    def __init__(self) -> None:
        pass

    def execute(self):
        # this will run parellaly
        pass

    def filter(self, all_candle_events: dict[str, list[CandleEvent]]) -> bool:
        # no api will be called here as it will run syncronusly
        # no logic which have high processing time will be called here
        return False

    def set_db(self, db: Db):
        self.db = db

    def set_exchange(self, exchange: Exchange):
        self.exchange = exchange
