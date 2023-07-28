
from src.models.enums import INTERVAL_TYPE


class CandleEvent:

    '''
    Ex:
    {
        symbol: "BTC",
        interval: M5,
        updated: [1234, 1235], #timestamps
        inserted: [1236],
        generated: True
    }
    '''

    def __init__(self, symbol: str, interval: INTERVAL_TYPE, generated: bool) -> None:
        self.symbol = symbol
        self.interval = interval
        self.updated = []
        self.inserted = []
        self.generated = generated

    def add_to_inserted(self, inserted: int):
        self.inserted.append(inserted)
    
    def add_to_inserted_as_list(self, inserted_list: list[int]):
        self.inserted.extend(inserted_list)

    def add_to_updated(self, updated: int):
        self.updated.append(updated)

    def get_start_end_time(self) -> tuple:
        if not self.updated and not self.inserted:
            # both empty
            return ()
        start_index = self.updated[0] if self.updated else self.inserted[0]
        end_index = self.inserted[-1] if self.inserted else self.updated[-1]
        return start_index, end_index

    def __repr__(self) -> str:
        return f"symbol: {self.symbol}; interval: {self.interval.name}; generated: {self.generated}; updated: {self.updated}; inserted: {self.inserted}"
