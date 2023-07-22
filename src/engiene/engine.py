import threading
import schedule
import time
from datetime import datetime
from src.engiene.indicator_manager import IndicatorManager
from src.engiene.strategy_manager import StrategyManager
from src.exchange.quote_service import QuoteService
from src.engiene.candle_manager import CandleManager
from src.models.market_watch import MarketWatch
from src.models.enums import INTERVAL_TYPE
from src.engiene.engine_config import EngineConfig, SymbolConfig
from src.strategy.strategy import Strategy


class Engine(threading.Thread):

    def __init__(self, configs) -> None:
        threading.Thread.__init__(self, name="engine_thread", daemon=True)
        self.configs = EngineConfig(configs)
        self.market_watch = MarketWatch(self.configs)
        self.candle_manager = CandleManager(self.market_watch)
        self.indicator_manager = IndicatorManager(self.market_watch)
        self.quote_service = QuoteService()
        self.strategy_manager = StrategyManager(Strategy())

    def run(self):
        # get history candles and indicators
        self.get_history_all()
        # configure scheduler
        # schedule.every(5).minutes.at(":05").do(self.run_scheduler)
        schedule.every(5).seconds.do(self.run_scheduler)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def get_history_all(self):
        print("inside get_history_all")
        current_time = datetime.now()
        calls = []
        for config in self.configs.get_all_configs():
            calls.append(threading.Thread(
                target=self.get_history_symbol, args=(config, current_time), daemon=True))
        for call in calls:
            call.start()
        for call in calls:
            call.join()

    def get_history_symbol(self, config: SymbolConfig, current_time):
        # get history candles and indicators per symbol and add to state
        print("get_history_symbol", config.symbol())

    def get_current_symbol(self, config: SymbolConfig, current_time):
        print("get_current_symbol", config.symbol())
        # get current candles and indicators and add to state
        curr_candles = self.quote_service.get_candles(
            config.symbol(), config.current_intervals()[0], current_time, config.current_candles_no())
        print(curr_candles)
        candle_event = self.candle_manager.create_upadte_candles(
            curr_candles, config)
        # print(candle_event)
        self.indicator_manager.create_upadte_indicators(candle_event)
        self.strategy_manager.notify(candle_event)

    def run_scheduler(self):
        print("schedluer ran at", datetime.now())
        self.get_current_all()
        # self.run_strategy_all() #todo

    def get_current_all(self):
        calls = []
        current_time = datetime.now()
        for config in self.configs.get_all_configs():
            calls.append(threading.Thread(
                target=self.get_current_symbol, args=(config, current_time), daemon=True))
        for call in calls:
            call.start()
        for call in calls:
            call.join()
