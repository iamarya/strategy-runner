
from src.engiene.engine_config import EngineConfig
from src.models.event import CandleEvent
from src.strategy.strategy import Strategy
'''
strategy_config = {
	# strategy1 to symbol 1 to 1 per therad
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
    def __init__(self, engine_config: EngineConfig) -> None:
        self.strategies = []
    
    def notify(self, all_candle_events:dict[str, list[CandleEvent]])-> list[Strategy]:
        # notify will run every sec # all_candle_eventsmay come empty, that time check if strategy need to run based on time
        # if its not empty then check for symbol and interval which strategies need to called
        strategies_torun = []
        for strategy in self.strategies:
            if strategy.is_ready(all_candle_events):
                strategies_torun.append(strategy)
        return strategies_torun
    
    def run(self, strategy:Strategy, all_candle_events:dict[str, list[CandleEvent]]):
        strategy.execute(all_candle_events)