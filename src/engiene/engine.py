from threading import Thread
from src.engiene.engine_config import configs
import schedule
import time
import datetime
import asyncio

class Engine(Thread):

    def __init__(self) -> None:
        Thread.__init__(self, daemon=True)
    
    def run(self):
        # get history candles
        asyncio.run(self.get_history_all())
        # configure scheduler
        #schedule.every(5).minutes.at(":05").do(self.run_scheduler)
        schedule.every(5).seconds.do(self.run_scheduler)
        while True:
            schedule.run_pending()
            time.sleep(1)

    async def get_history_all(self):
        print("inside getHistoryAll")
        calls = []
        for config in configs:
            calls.append(self.get_history_symbol(config["symbol"]))
        await asyncio.gather(*calls)
    
    async def get_history_symbol(self, symbol:str):
        print("symbol", symbol)

    def run_scheduler(self):
        print("schedluer ran at", datetime.datetime.now())

