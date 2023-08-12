import logging

from models.event_queue import EventQueue
from services.market_watch_service import MarketWatch
from services.orderbook_service import OrderBookService
from strategy.strategy import Strategy

logger = logging.getLogger(__name__)

'''
strategy_config = {
    # strategy1 to symbol 1? to 1 per thread
        # i think always run one instance of strategy and call in a loop for all symbols it needs
        # one strategy needs one sheet so should not multithread this
    # but dont create thread if not used by strategy so some config needed
    # this config may need to have interval a particular interval/s 
}

candle_event_value  = 
{'BTC':
    [{
        symbol: "BTC",
        interval: M5,
        updated: [1234, 1235], #timestamps
        inserted: [1236]
    },
    {
        symbol: "BTC",
        interval: D1,
        updated: [1234, 1235], #timestamps
        inserted: [1236]
    }],
'TCS':
    [{
        symbol: "TCS",
        interval: M5,
        updated: [1234, 1235], #timestamps
        inserted: [1236]
    },
    {
        symbol: "TCS",
        interval: D1,
        updated: [1234, 1235], #timestamps
        inserted: [1236]
    }]
}
'''


class StrategyManager:
    def __init__(self, strategies: list[Strategy], event_queue: EventQueue,
                 market_watch: MarketWatch, order_book_service: OrderBookService) -> None:
        self.strategies: list[Strategy] = strategies  # register strategies
        for strategy in self.strategies:
            strategy.set_market_watch(market_watch)
            strategy.set_records(order_book_service.get_records(strategy.name))
        self.event_queue = event_queue

    def notify(self) -> list[Strategy]:
        # notify will run every sec # all_candle_events may come empty,
        # that time check if strategy need to run based on time
        # if its not empty then check for symbol and interval which strategies need to called
        strategies_torun: list[Strategy] = []
        logger.debug("get notified")
        event = self.event_queue.pull()
        if event is None:
            return []
        logger.debug('event_candles %s %s', event.type, event.value)
        for strategy in self.strategies:
            if strategy.filter(event):
                strategies_torun.append(strategy)
        # return strategy and its event pair
        return strategies_torun

        # this logic wil run parallel for each filter strategy periodically

    def run(self, strategy: Strategy):
        if strategy in self.strategies:
            strategy.execute()
