
from src.models.enums import INTERVAL_TYPE


class CandleEvent:

    def __init__(self, symbol: str, interval: INTERVAL_TYPE) -> None:
        self.symbol = symbol
        self.interval = interval
        self.updated = []
        self.inserted = []

    def add_to_inserted(self, inserted: int):
        self.inserted.append(inserted)

    def add_to_updated(self, updated: int):
        self.updated.append(updated)

    def __repr__(self) -> str:
        return f"symbol: {self.symbol}; interval: {self.interval.name}; updated: {self.updated}; inserted: {self.inserted}"
