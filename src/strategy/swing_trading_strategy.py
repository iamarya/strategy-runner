import logging

from models.candle_update_detail import CandleUpdateDetail
from models.enums import *
from models.event import Event
from strategy.strategy import Strategy

logger = logging.getLogger(__name__)

symbol_to_trade = 'BTCUSDT'
interval = INTERVAL_TYPE.S5
indicators = ("sma_8", "sma_13")
buy_window = ('', '')
sell_window = ('', '')
exit_window = ('', '')

buy_price = 0
sell_price = 0
total_profit = 0


# strategies are stateful in nature, don't share between threads
class SwingTradingStrategy(Strategy):

    def __init__(self) -> None:
        Strategy.__init__(self)
        logger.warning("SwingTradingStrategy deployed")
        self.event_candle = None
        self.action = None
        self.state = STATE.START

    # this called in a separate thread
    def execute(self):
        # todo check NaN for value from market watch | call a validate method as 1st line
        global buy_price, sell_price, total_profit
        assert self.event_candle is not None
        time = self.event_candle.inserted[0]
        df = self.market_watch_service.get_candles(symbol_to_trade, interval)
        sma_8 = df.loc[time]['sma_8']
        sma_13 = df.loc[time]['sma_13']
        price = df.loc[time]['close']
        logger.debug("SwingTradingStrategy executed %s, %s, %s, %s", self.action, sma_8, sma_13, price)
        if self.action == ACTION.BUY:
            if sma_8 > sma_13:
                self.state = STATE.BUY_CONFIRMED
                buy_price = price
                logger.warning("bought at %s", buy_price)
        if self.action == ACTION.SELL:
            if sma_8 < sma_13:
                self.state = STATE.START
                sell_price = price
                profit = sell_price - buy_price
                logger.warning(f"sold at {sell_price} profit: {profit}")
                total_profit = total_profit + profit
                logger.warning("total profit: %s ", total_profit)

    # no http api sh call inside filter as it's not executed in separate thread
    # todo decide if market watch can be accessed from filter
    def filter(self, event: Event) -> bool:
        logger.debug("SwingTradingStrategy filter")
        if event.type != EVENT_TYPE.CANDLE_EVENT or not event.value:
            return False
        all_candle_update_details: dict[str, list[CandleUpdateDetail]] = event.value
        for event_candle in all_candle_update_details[symbol_to_trade]:
            if event_candle.interval == INTERVAL_TYPE.S5 and event_candle.inserted:
                self.event_candle = event_candle
                if self.state == STATE.START:
                    self.action = ACTION.BUY
                elif self.state == STATE.BUY_CONFIRMED:
                    self.action = ACTION.SELL
                return True
        return False
