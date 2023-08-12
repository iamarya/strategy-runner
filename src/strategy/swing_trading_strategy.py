import logging

import numpy as np

from models.candle_update_detail import CandleUpdateDetail
from models.enums import *
from models.event import Event
from strategy.strategy import Strategy

logger = logging.getLogger(__name__)

# need to create a config kind of object
symbol_to_trade = 'BTCUSDT'  # can be list for some strategy
interval = INTERVAL_TYPE.M15
indicators = ("sma_9", "sma_21")
buy_window = ('', '')
sell_window = ('', '')
exit_window = ('', '')

# will be removed once db is used
buy_price = 0
sell_price = 0
total_profit = 0


# todo strategy will call order service and pass the exchange in method argument
# both exchange and order service will be a attribute of the strategy
# for now exchange for a single type is singleton (can it be not singleton?)
# services also singleton but stateless

# strategies are stateful in nature, don't share between threads
class SwingTradingStrategy(Strategy):

    def __init__(self) -> None:
        Strategy.__init__(self, 'swing_trading_strategy')
        logger.warning("SwingTradingStrategy deployed")
        self.event_candle: CandleUpdateDetail | None = None
        self.action = None # also not needed if can be derived from state
        self.status = STATE.START # may be not needed
        self.state = None # may be not needed
        # self.records is only needed

    # this called in a separate thread
    def execute(self):
        global buy_price, sell_price, total_profit
        if self.event_candle is None or not self.event_candle.inserted:
            return
        latest_time = self.event_candle.inserted[-1]
        # get the previous candle of just inserted, todo write a service method for this
        df = self.market_watch.get_candles(symbol_to_trade, interval)
        index_of_current_time = df.index.get_loc(latest_time)
        if index_of_current_time == 0:
            return  # 1st candle no previous so exit
        time = df.iloc[index_of_current_time - 1].name
        cols = df.columns.to_list()
        if indicators[0] not in cols or indicators[1] not in cols:
            logger.debug('sma_low or sma_high col not there')
            return
        sma_low = df.loc[time][indicators[0]]
        sma_high = df.loc[time][indicators[1]]
        price = df.loc[time]['close']
        # check NaN for value from market watch | call a validate method as 1st line
        if np.isnan([sma_low, sma_high, price]).any():
            logger.debug("skipped as value are nan %s, sma_low: %s, sma_high: %s, price: %s", self.action, sma_low,
                         sma_high,
                         price)
            return

        logger.debug("executed %s, sma_low: %s, sma_high: %s, price: %s, state: %s", self.action, sma_low, sma_high, price, self.status)
        if self.action == ACTION.BUY:
            if sma_low > sma_high:
                self.status = STATE.BUY_CONFIRMED
                buy_price = price
                logger.info("bought at %s", buy_price)
        if self.action == ACTION.SELL:
            if sma_low < sma_high:
                self.status = STATE.START
                sell_price = price
                profit = sell_price - buy_price
                logger.info(f"sold at {sell_price} profit: {profit}")
                total_profit = total_profit + profit
                logger.info("total profit: %s ", total_profit)

    # no http api sh call inside filter as it's not executed in separate thread
    # todo decide if market watch can be accessed from filter
    # check window, event, if event has symbol and interval needed
    def filter(self, event: Event) -> bool:
        logger.debug("SwingTradingStrategy filter")
        if event.type != EVENT_TYPE.CANDLE_EVENT or not event.value:
            return False
        all_candle_update_details: dict[str, list[CandleUpdateDetail]] = event.value
        for event_candle in all_candle_update_details[symbol_to_trade]:
            if event_candle.interval == interval and event_candle.inserted:
                self.event_candle = event_candle
                if self.status == STATE.START:
                    self.action = ACTION.BUY
                elif self.status == STATE.BUY_CONFIRMED:
                    self.action = ACTION.SELL
                return True
        return False
