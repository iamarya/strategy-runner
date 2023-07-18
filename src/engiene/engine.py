import threading
import schedule
import time
from datetime import datetime
from src.exchange.quote_service import QuoteService
from src.models.enums import Duration


class Engine(threading.Thread):

    def __init__(self, configs) -> None:
        threading.Thread.__init__(self, name="engine_thread", daemon=True)
        self.quote_service = QuoteService()
        self.configs = configs

    def run(self):
        # get history candles
        self.get_history_all()
        # configure scheduler
        # schedule.every(5).minutes.at(":05").do(self.run_scheduler)
        schedule.every(5).seconds.do(self.run_scheduler)
        while True:
            schedule.run_pending()
            time.sleep(1)

    def get_history_all(self):
        print("inside get_history_all")
        calls = []
        for config in self.configs["symbols"]:
            calls.append(threading.Thread(
                target=self.get_history_symbol, args=(config["symbol"],), daemon=True))
        for call in calls:
            call.start()
        for call in calls:
            call.join()

    def get_history_symbol(self, symbol: str):
        print("get_history_symbol", symbol)

    def get_current_symbol(self, symbol: str):
        print("get_current_symbol", symbol)
        self.quote_service.get_currect_candle(
            symbol, Duration.M5, datetime.now())

    def run_scheduler(self):
        print("schedluer ran at", datetime.now())
        self.get_current_all()
        # self.run_strategy_all()

    def get_current_all(self):
        calls = []
        now = time.time()
        for config in self.configs["symbols"]:
            calls.append(threading.Thread(
                target=self.get_current_symbol, args=(config["symbol"],), daemon=True))
        for call in calls:
            call.start()
        for call in calls:
            call.join()
