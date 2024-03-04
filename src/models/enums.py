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

# todo: event type can be removed, as timer event is not needed.
# all events are candle event and "TIMER" candle will be created. From event also type will be removed.
class EVENT_TYPE(Enum):
    CANDLE_EVENT = 1
    TIMER_EVENT = 2


class TRANSACTION_TYPE(Enum):
    BUY = 1
    SELL = 2

class ORDER_TYPE(Enum):
    MARKET = 1
    LIMIT = 2
    SL_MARKET = 3
    SL_LIMIT = 4


class STATE(Enum):
    PENDING = 2
    CONFIRMED = 3
    CANCELED = 4
    EXITED = 8


class ACTION(Enum):
    BUY = 1
    BUY_CONFIRM = 2
    BUY_CANCEL = 3
    SELL = 4
    SELL_CONFIRM = 5
    SELL_CANCEL = 6
    EXIT = 7
    # todo an idea can action and state can be combined??


class MODE(Enum):
    LIVE = 1
    SANDBOX = 2
