from enum import Enum
from datetime import timedelta

class Interval:

    def __init__(self, time_delta, secs:int) -> None:
        self.time_delta = time_delta
        self.secs = secs

class INTERVAL_TYPE(Enum):

    M5 = Interval(timedelta(minutes=5), 300)
    M10 = Interval(timedelta(minutes=10), 600)
    HR1 = Interval(timedelta(hours=1), 3600)
    D1 = Interval(timedelta(days=1), 86400)

class EXCAHNGE_TYPE(Enum):
    MOCK_EXCAHNGE = 1
    COINBASE_EXCHANGE = 2
    BINANCE_EXCAHNGE = 3
    ZERODHA_EXCHANGE = 4

class DB_TYPE(Enum):
    IN_MEMORY = 1 
    G_SHEET = 2

class INDICATOR_TYPE(Enum):
    pass



    
