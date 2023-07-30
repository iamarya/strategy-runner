

from models.event import CandleEvent
from strategy.strategy import Strategy


class SwingTradingStrategy(Strategy):

    def __init__(self) -> None:
        Strategy.__init__(self)

    def execute(self, event:list[CandleEvent]):
        pass
