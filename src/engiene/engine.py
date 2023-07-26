import threading
import schedule
import time
from datetime import datetime
from src.models.event import CandleEvent
from src.engiene.indicator_manager import IndicatorManager
from src.engiene.strategy_manager import StrategyManager
from src.exchange.quote_service import QuoteService
from src.engiene.market_watch_manager import MarketWatchManager
from src.models.enums import INTERVAL_TYPE
from src.engiene.engine_config import EngineConfig, SymbolConfig
from src.strategy.strategy import Strategy


class Engine(threading.Thread):

    def __init__(self, engine_config) -> None:
        threading.Thread.__init__(self, name="engine_thread", daemon=True)
        self.engine_config = EngineConfig(engine_config)
        self.market_watch_manager = MarketWatchManager(self.engine_config)
        self.indicator_manager = IndicatorManager(self.market_watch_manager)
        self.quote_service = QuoteService()
        self.strategy_manager = StrategyManager(Strategy())
        self.all_candle_events = [] # todo may be better to make a dict()

    def run(self):
        # get history candles and indicators
        self.get_history_all()
        if not self.engine_config.is_backtest():
            # configure scheduler
            # schedule.every(5).minutes.at(":05").do(self.run_scheduler)
            schedule.every(5).seconds.do(self.run_scheduler)
            while True:
                schedule.run_pending()
                time.sleep(1)
        else:
            # backtesting only
            print("doing backtesting only")
            synthesized_all_candle_events_all_time = self.market_watch_manager.synthesized_all_candle_events_all_time()
            for all_candle_events_at_time in synthesized_all_candle_events_all_time:
                self.strategy_manager.notify(all_candle_events_at_time)

    def get_history_all(self):
        print("inside get_history_all")
        current_time = datetime.now()
        calls = []
        for symbols_config in self.engine_config.get_all_configs():
            for symbol in symbols_config.symbols:
                calls.append(threading.Thread(
                    target=self.get_history_symbol, args=(symbol, symbols_config.symbol_config, current_time), daemon=True))
        for call in calls:
            call.start()
        for call in calls:
            call.join()

    def get_history_symbol(self, symbol: str, config: SymbolConfig, current_time):
        # get history candles and indicators per symbol and add to state
        print("get_history_symbol", symbol)
        # candle_events = []
        for interval in config.history_intervals():
            history_candles = self.quote_service.get_candles(
                symbol, interval, current_time, config.history_candles_no())
            # print(curr_candles)
            candle_event = self.market_watch_manager.add_update_candles(symbol, interval,
                                                                        history_candles)
            self.create_update_indicators(config, candle_event)

    def get_current_symbol(self, symbol: str, config: SymbolConfig, current_time):
        print(f"--- get_current_symbol:{symbol} ---")
        # get current candles and indicators and add to state
        candle_events:list[CandleEvent] = []
        for interval in config.current_intervals():
            curr_candles = self.quote_service.get_candles(
                symbol, interval, current_time, config.current_candles_no())
            candle_event = self.market_watch_manager.add_update_candles(symbol, interval,
                                                                        curr_candles)
            candle_events.append(candle_event)
            self.create_update_indicators(config, candle_event)

        #todo write propercode to sort and get smallets interval as source and corrosponding candle event
        source_interval = config.current_intervals()[0]
        source_candle_event = candle_events[0]
        # generate candles
        for interval in config.current_intervals_generated():
            candle_event = self.market_watch_manager.generate_candles(symbol, source_interval, source_candle_event, interval)
            candle_events.append(candle_event)
            self.create_update_indicators(config, candle_event)
        # printing things
        self.market_watch_manager.print_market_watch(symbol)
        # candle_events: list[CandleEvent] is for a perticular time for all intervals for a single symbol
        print("candle_events:", candle_events)
        self.all_candle_events.append(candle_events)

    def create_update_indicators(self, config, candle_event):
        for indicator in config.indicators():
            self.indicator_manager.create_upadte_indicators(
                    candle_event, indicator)

    def run_scheduler(self):
        print(f"\n\n === Schedluer Triggered @ {datetime.now()} ===\n")
        self.all_candle_events = []
        self.get_current_all()
        self.strategy_manager.notify(self.all_candle_events)

    def get_current_all(self):
        calls = []
        current_time = datetime.now()
        for symbols_config in self.engine_config.get_all_configs():
            for symbol in symbols_config.symbols:
                calls.append(threading.Thread(
                    target=self.get_current_symbol, args=(symbol, symbols_config.symbol_config, current_time), daemon=True))
        for call in calls:
            call.start()
        for call in calls:
            call.join()
        print('Time talen to run fetch all quotes', datetime.now() - current_time)
