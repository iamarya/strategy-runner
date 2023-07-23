

from src.models.event import CandleEvent
from src.strategy.strategy import Strategy


class SwingTradingStrategy(Strategy):

    def __init__(self) -> None:
        pass

    def execute(self, event:list[CandleEvent]):
        pass
