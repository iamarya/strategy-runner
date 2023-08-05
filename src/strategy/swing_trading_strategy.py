from models.enums import INTERVAL_TYPE
from models.candle_update_detail import CandleUpdateDetail
from models.event import Event
from strategy.strategy import Strategy
from models.enums import *

symbol_to_trade = 'BTCUSDT'
interval = INTERVAL_TYPE.S5
indicators = ("sma_8","sma_13")
buy_window = ('', '')
sell_window = ('', '')
exit_window = ('', '')

buy_price = 0
sell_price = 0
total_profit = 0

# strategies are stateful in nature, dont share between threads
class SwingTradingStrategy(Strategy):

    def __init__(self) -> None:
        Strategy.__init__(self)
        self.event_candle = None
        self.action = None
        self.state = STATE.START

    # this called in a seprate thread
    def execute(self):
        
        global buy_price, sell_price, total_profit
        assert self.event_candle is not None
        time = self.event_candle.inserted[0]
        df = self.market_watch_service.get_candles(symbol_to_trade, interval)
        sma_8 = df.loc[time]['sma_8']
        sma_13 = df.loc[time]['sma_13']
        price = df.loc[time]['close']
        print("SwingTradingStrategy executed", self.action, sma_8, sma_13, price)
        if self.action == ACTION.BUY:
            if sma_8 > sma_13:
                self.state = STATE.BUY_CONFIRMED
                buy_price = price
                print("bought at ", buy_price)
        if self.action == ACTION.SELL:
            if sma_8 < sma_13:
                self.state = STATE.START
                sell_price = price
                profit = sell_price - buy_price
                print("sold at ", sell_price, " profit:", profit)
                total_profit = total_profit + profit
                print("total profit: ", total_profit)


    # no http api sh call inside filter as its not executed in separate thread
    def filter(self, event: Event) -> bool:
        print("SwingTradingStrategy filter")
        if event.type != EVENT_TYPE.CANDLE_EVENT or not event.value:
            print("returned false from line 61")
            return False
        all_candle_update_details: dict[str, list[CandleUpdateDetail]] = event.value 
        for event_candle in all_candle_update_details[symbol_to_trade]:
            if event_candle.interval == INTERVAL_TYPE.S5 and event_candle.inserted:
                self.event_candle = event_candle
                if self.state == STATE.START:
                    self.action = ACTION.BUY
                elif self.state == STATE.BUY_CONFIRMED:
                    self.action = ACTION.SELL
                print("returned true from line 71")
                return True
        print("returned false from line 73")
        return False
