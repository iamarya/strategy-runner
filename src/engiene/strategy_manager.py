
import datetime
from models.event_queue import EventQueue
from config.engine_config import EngineConfig
from models.event import CandleEvent
from strategy.strategy import Strategy
'''
strategy_config = {
	# strategy1 to symbol 1? to 1 per therad
    	# i think always run one instance of strategy and call in a loop for all symbols it needs
        # one strategy needs one sheet so should not multithread this
	# but dont create thread if not used by strategy so some config needed
    # this config may need to have interval a perticular interval/s 

}

all_candle_events  = 
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
    def __init__(self, strategies: list[Strategy], event_queue: EventQueue) -> None:
        self.strategies: list[Strategy] = strategies  # register stratageies
        self.event_queue = event_queue

    def notify(self) -> list[tuple]:
        # notify will run every sec # all_candle_eventsmay come empty, that time check if strategy need to run based on time
        # if its not empty then check for symbol and interval which strategies need to called
        strategies_torun: list[tuple] = []
        print("get notified")
        all_candle_events = self.event_queue.pull()
        print('all_candle_events', all_candle_events)
        for strategy in self.strategies:
            if strategy.filter(all_candle_events):
                print(all_candle_events)
                strategies_torun.append((strategy, all_candle_events['BTC']))
        # return strategy and its event pair
        return strategies_torun

        # this logic wil run paralelly for each filter strategy periodically
    def run(self, strategy: Strategy, event: list[tuple]):
        strategy.execute(event)  # type: ignore
