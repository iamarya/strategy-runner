

from src.models.event import CandleEvent


class Strategy:

    def __init__(self) -> None:
        pass

    def execute(self, all_candle_events: dict[str, list[CandleEvent]]):
        pass

    def is_ready(self, all_candle_events: dict[str, list[CandleEvent]]) -> bool:
        return True
