from abc import abstractmethod

from db.db import Db
from exchange.exchange import Exchange
from models.event import Event
from models.market_watch import MarketWatch


class Strategy:

    def __init__(self) -> None:
        pass

    @abstractmethod
    def execute(self):
        # this will run parellaly
        pass

    @abstractmethod
    def filter(self, event: Event) -> bool:
        # no api will be called here as it will run syncronusly
        # no logic which have high processing time will be called here
        return False

    def set_db(self, db: Db):
        # todo as getter also and initialise as none this attributes in constructor
        # getter you can write assert to avoid None return
        self.db = db

    def set_exchange(self, exchange: Exchange):
        self.exchange = exchange
        
    def set_market_watch(self, market_watch: MarketWatch):
        self.market_watch = market_watch