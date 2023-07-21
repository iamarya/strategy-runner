import threading
import schedule
import time
from datetime import datetime
from src.exchange.quote_service import QuoteService
from src.engiene.candle_manager import CandleManager
from src.models.market_watch import MarketWatch
from src.models.enums import INTERVAL_TYPE


class Engine(threading.Thread):

    def __init__(self, configs) -> None:
        threading.Thread.__init__(self, name="engine_thread", daemon=True)
        self.quote_service = QuoteService()
        self.market_watch = MarketWatch(configs)
        self.candle_manager = CandleManager(self.market_watch)
        self.configs = configs

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
        for config in self.configs["symbols"]:
            calls.append(threading.Thread(
                target=self.get_history_symbol, args=(config, current_time), daemon=True))
        for call in calls:
            call.start()
        for call in calls:
            call.join()

    def get_history_symbol(self, config, current_time):
        # get history candles and indicators per symbol and add to state
        print("get_history_symbol", config["symbol"])

    def get_current_symbol(self, config, current_time):
        print("get_current_symbol", config["symbol"])
        # get current candles and indicators and add to state
        curr_candles = self.quote_service.get_candles(
            config["symbol"], config["current_intervals"][0], current_time, config["current_candles_no"])
        print(curr_candles)
        self.candle_manager.create_upadte_candles(curr_candles)
        # self.indicator_manager.create_upadte_indicators(curr_candles)

    def run_scheduler(self):
        print("schedluer ran at", datetime.now())
        self.get_current_all()
        # self.run_strategy_all() #todo

    def get_current_all(self):
        calls = []
        current_time = datetime.now()
        for config in self.configs["symbols"]:
            calls.append(threading.Thread(
                target=self.get_current_symbol, args=(config, current_time), daemon=True))
        for call in calls:
            call.start()
        for call in calls:
            call.join()
