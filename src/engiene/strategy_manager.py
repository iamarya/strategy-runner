
from src.models.event import CandleEvent
from src.strategy.strategy import Strategy
'''
strategy_config = {
	# strategy1 to symbol 1 to 1 per therad
	# but dont create thread if not used by strategy so some config needed
    # this config may need to have interval a perticular interval/s 

}

events  = [
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
}]
,
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
]
'''
class StrategyManager:
    def __init__(self, strategies: Strategy) -> None:
        # register strategies
        pass

    def notify(self, candle_events:list[list[CandleEvent]]):
        pass
