

from models.event import CandleEvent
from strategy.strategy import Strategy


class SwingTradingStrategy(Strategy):

    def __init__(self) -> None:
        pass

    def execute(self, event:list[CandleEvent]):
        pass
