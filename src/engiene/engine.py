from threading import Thread
from src.engiene.engine_config import configs
import schedule
import time
from datetime import datetime
import asyncio
from src.exchange.quote_service import QuoteService
from src.models.enums import Duration


class Engine(Thread):

    def __init__(self) -> None:
        Thread.__init__(self, name="engine_thread", daemon=True)
        self.quote_service = QuoteService()

    def run(self):
        # get history candles
        asyncio.run(self.get_history_all())
        # configure scheduler
        # schedule.every(5).minutes.at(":05").do(self.run_scheduler)
        schedule.every(5).seconds.do(self.run_scheduler)
        while True:
            schedule.run_pending()
            time.sleep(1)

    async def get_history_all(self):
        print("inside get_history_all")
        calls = []
        for config in configs["symbols"]:
            calls.append(self.get_history_symbol(config["symbol"]))
        await asyncio.gather(*calls)

    async def get_history_symbol(self, symbol: str):
        print("get_history_symbol", symbol)
        return

    async def get_current_symbol(self, symbol: str):
        print("get_current_symbol", symbol)
        self.quote_service.get_currect_candle(symbol, Duration.M5, datetime.now())

    def run_scheduler(self):
        asyncio.run(self.get_current_all())
        print("schedluer ran at", datetime.now())

    async def get_current_all(self):
        calls = []
        now = time.time()
        for config in configs["symbols"]:
            calls.append(self.get_current_symbol(config["symbol"]))
        await asyncio.gather(*calls)
