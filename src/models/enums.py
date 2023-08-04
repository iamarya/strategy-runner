from enum import Enum, IntEnum

# IntEnum for comparing enum type <, >


class INTERVAL_TYPE(IntEnum):
    S5 = 5  # testing purpose
    M5 = 300
    M15 = 900
    HR1 = 3600
    D1 = 86400
    W1 = 604800

    def __repr__(self) -> str:
        return self.name


class EXCAHNGE_TYPE(Enum):
    MOCK_EXCAHNGE = 1
    COINBASE_EXCHANGE = 2
    BINANCE_EXCAHNGE = 3
    ZERODHA_EXCHANGE = 4
    CSV_EXCHANGE = 5

    def __repr__(self) -> str:
        return self.name


class DB_TYPE(Enum):
    IN_MEMORY = 1
    G_SHEET = 2

    def __repr__(self) -> str:
        return self.name


class EVENT_TYPE(Enum):
    CANDLE_EVENT = 1
    TIMER_EVENT = 2


class STATE(Enum):
    START = 1
    BUY_PENDING = 2
    BUY_CONFIRMED = 3
    BUY_CANCELED = 4
    SELL_PENDING = 5
    SELL_CONFIRMED = 6
    SELL_CANCELED = 7
    EXITED = 8
    SL_TRIGGERED = 9
    END = 10


class ACTION(Enum):
    BUY = 1
    BUY_CONFIRM = 2
    BUY_CANCEL = 3
    SELL = 4
    SELL_CONFIRM = 5
    SELL_CANCEL = 6
    EXIT = 7

class MODE(Enum):
    LIVE = 1
    SANDBOX = 2
