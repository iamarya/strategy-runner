

from db.db import Db
from exchange.exchange import Exchange
from models.event import Event
from services.market_watch_service import MarketWatchService


class Strategy:

    def __init__(self) -> None:
        pass

    def execute(self):
        # this will run parellaly
        pass

    def filter(self, event: Event) -> bool:
        # no api will be called here as it will run syncronusly
        # no logic which have high processing time will be called here
        return False

    def set_db(self, db: Db):
        self.db = db

    def set_exchange(self, exchange: Exchange):
        self.exchange = exchange
        
    def set_market_watch_service(self, market_watch_service: MarketWatchService):
        self.market_watch_service = market_watch_service