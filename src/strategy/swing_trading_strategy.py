from models.enums import INTERVAL_TYPE
from models.candle_update_detail import CandleUpdateDetail
from models.event import Event
from strategy.strategy import Strategy
from models.enums import *

symbol_to_trade = 'BTCUSDT'


# strategies are stateful in nature, dont share between threads
class SwingTradingStrategy(Strategy):

    def __init__(self) -> None:
        Strategy.__init__(self)
        self.event_candle = None
        self.action = None
        self.state = STATE.START

    # this called in a seprate thread
    def execute(self):
        print("SwingTradingStrategy executed")

    # no http api sh call inside filter as its not executed in separate thread
    def filter(self, event: Event) -> bool:
        all_candle_update_details = event.value
        if not all_candle_update_details:
            return False
        for event_candle in all_candle_update_details[symbol_to_trade]:
            if event_candle.interval == INTERVAL_TYPE.S5:
                self.event_candle = event_candle
                self.action = ACTION.BUY
                return True
        return False
