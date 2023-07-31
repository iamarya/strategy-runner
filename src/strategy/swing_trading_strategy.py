from models.enums import INTERVAL_TYPE
from models.event import CandleEvent
from strategy.strategy import Strategy
from models.enums import *

symbol_to_trade = 'BTC'


# strategies are stateful in nature, dont share between threads
class SwingTradingStrategy(Strategy):

    def __init__(self) -> None:
        Strategy.__init__(self)
        self.candle_event = None
        self.action = None
        self.state = STATE.START

    # this called in a seprate thread
    def execute(self):
        print("SwingTradingStrategy executed")

    # no http api sh call inside filter as its not executed in separate thread
    def filter(self, all_candle_events: dict[str, list[CandleEvent]]) -> bool:
        if not all_candle_events:
            return False
        for e in all_candle_events[symbol_to_trade]:
            if e.interval == INTERVAL_TYPE.S5:
                self.candle_event = e
                self.action = ACTION.BUY
                return True
        return False
