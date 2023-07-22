from enum import Enum


class INTERVAL_TYPE(Enum):
    S5 = 5  # testing purpose
    M5 = 300
    M10 = 600
    HR1 = 3600
    D1 = 86400

    def __repr__(self) -> str:
        return self.name


class EXCAHNGE_TYPE(Enum):
    MOCK_EXCAHNGE = 1
    COINBASE_EXCHANGE = 2
    BINANCE_EXCAHNGE = 3
    ZERODHA_EXCHANGE = 4

    def __repr__(self) -> str:
        return self.name


class DB_TYPE(Enum):
    IN_MEMORY = 1
    G_SHEET = 2

    def __repr__(self) -> str:
        return self.name


class INDICATOR_TYPE(Enum):
    pass
