import threading
import schedule
import time
from datetime import datetime
from src.engiene.indicator_manager import IndicatorManager
from src.engiene.strategy_manager import StrategyManager
from src.exchange.quote_service import QuoteService
from src.engiene.market_watch_manager import MarketWatchManager
from src.models.enums import INTERVAL_TYPE
from src.engiene.engine_config import EngineConfig, SymbolConfig
from src.strategy.strategy import Strategy


class Engine(threading.Thread):

    def __init__(self, configs) -> None:
        threading.Thread.__init__(self, name="engine_thread", daemon=True)
        self.configs = EngineConfig(configs)
        self.market_watch_manager = MarketWatchManager(self.configs)
        self.indicator_manager = IndicatorManager(self.market_watch_manager)
        self.quote_service = QuoteService()
        self.strategy_manager = StrategyManager(Strategy())

    def run(self):
        # get history candles and indicators
        self.get_history_all()
        if not self.configs.is_backtest():
            # configure scheduler
            # schedule.every(5).minutes.at(":05").do(self.run_scheduler)
            schedule.every(5).seconds.do(self.run_scheduler)
            while True:
                schedule.run_pending()
                time.sleep(1)
        if self.configs.is_backtest():
            synthesized_all_candle_events = self.market_watch_manager.synthesize_all_candle_events()
            for candle_events in synthesized_all_candle_events:
                self.strategy_manager.notify(candle_events)

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
        # candle_events = []
        for interval in config.history_intervals():
            history_candles = self.quote_service.get_candles(
                config.symbol(), interval, current_time, config.history_candles_no())
            # print(curr_candles)
            candle_event = self.market_watch_manager.add_update_candles(config.symbol(), interval,
                                                                     history_candles)
            for indicator in config.indicators():
                self.indicator_manager.create_upadte_indicators(
                    candle_event, indicator)


    def get_current_symbol(self, config: SymbolConfig, current_time):
        print("get_current_symbol", config.symbol())
        # get current candles and indicators and add to state
        candle_events = []
        for interval in config.current_intervals():
            curr_candles = self.quote_service.get_candles(
                config.symbol(), interval, current_time, config.current_candles_no())
            # print(curr_candles)
            candle_event = self.market_watch_manager.add_update_candles(config.symbol(), interval,
                                                                     curr_candles)
            candle_events.append(candle_event)
            # add update indicators for given interval
            for indicator in config.indicators():
                self.indicator_manager.create_upadte_indicators(
                    candle_event, indicator)
        # print(candle_events)
        self.strategy_manager.notify(candle_events)

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
