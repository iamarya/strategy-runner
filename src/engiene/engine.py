import os
import threading
import schedule
import time
from datetime import datetime
from models.event_queue import EventQueue
from models.event import CandleEvent
from engiene.indicator_manager import IndicatorManager
from engiene.strategy_manager import StrategyManager
from engiene.market_watch_manager import MarketWatchManager
from models.enums import INTERVAL_TYPE
from config.engine_config import EngineConfig, SymbolConfig
from services.quote_service import QuoteService
from strategy.strategy import Strategy
import utils.market_watch_utils as market_watch_utils


class Engine(threading.Thread):

    def __init__(self, engine_config: EngineConfig) -> None:
        threading.Thread.__init__(self, name="engine_thread", daemon=True)
        self.engine_config = engine_config
        self.market_watch_manager = MarketWatchManager(self.engine_config)
        self.indicator_manager = IndicatorManager(self.market_watch_manager)
        self.quote_service = QuoteService()
        self.event_queue = EventQueue()
        self.strategy_manager = StrategyManager(
            self.engine_config.get_strategies(), self.event_queue)
        self.all_candle_events: dict[str, list[CandleEvent]] = {}

    def run(self):
        # get history candles and indicators
        self.get_history_all()
        threading.Thread(target=self.run_strategies, args=(),
                         daemon=True, name='run_strategies').start()
        if not self.engine_config.is_backtest():
            # configure scheduler
            # schedule.every(5).minutes.at(":05").do(self.run_market_watch_scheduler)
            schedule.every(5).seconds.do(self.run_market_watch_scheduler)
            while True:
                self.all_candle_events = {}
                schedule.run_pending()
                time.sleep(1)
        else:
            # backtesting only
            print("doing backtesting only")
            synthesized_all_candle_events_all_time = self.market_watch_manager.synthesized_all_candle_events_all_time()
            for all_candle_events_at_time in synthesized_all_candle_events_all_time:
                self.event_queue.push(all_candle_events_at_time)

    # todo move this to stratgey_runner
    def run_strategies(self):
        while True:
            current_time = datetime.now()
            strategies = self.strategy_manager.notify()

            calls = []
            for strategy in strategies:
                calls.append(threading.Thread(
                    target=self.strategy_manager.run, args=(strategy,), daemon=True))
            for call in calls:
                call.start()
            for call in calls:
                call.join()
            if strategies:
                print('Time taken to run run_pending_strategies',
                      datetime.now() - current_time)
            time.sleep(1)

    # todo all this to market_runner
    def get_history_all(self):
        print("inside get_history_all")
        # incase of data extractio or backtesting it might be some past date
        current_time = datetime.now()
        calls = []
        for symbols_config in self.engine_config.get_symbols_configs():
            for symbol in symbols_config.symbols:
                calls.append(threading.Thread(
                    target=self.get_history_symbol, args=(symbol, symbols_config.symbol_config, current_time), daemon=True))
        for call in calls:
            call.start()
        for call in calls:
            call.join()
        print('Time taken to run get_history_all',
              datetime.now() - current_time)

    def get_history_symbol(self, symbol: str, config: SymbolConfig, current_time):
        try:
            # get history candles and indicators per symbol and add to state
            print(f"--- get_history_symbol:{symbol} ---")
            candle_events = self.populate_market_watch(
                symbol, config, current_time, True)
            self.all_candle_events[symbol] = candle_events
        except:
            os._exit(0)

    def get_current_symbol(self, symbol: str, config: SymbolConfig, current_time):
        print(f"--- get_current_symbol:{symbol} ---")
        try:
            candle_events = self.populate_market_watch(
                symbol, config, current_time, False)
            self.all_candle_events[symbol] = candle_events
        except:
            os._exit(0)

    def populate_market_watch(self, symbol, config, current_time, is_history):
        if is_history:
            intervals = sorted(config.history_intervals())
            intervals_generated = sorted(config.history_intervals_generated())
            candles_no = config.history_candles_no()
        else:
            intervals = sorted(config.current_intervals())
            intervals_generated = sorted(config.current_intervals_generated())
            candles_no = config.current_candles_no()

        candle_events: list[CandleEvent] = []
        all_intervals = sorted(
            config.current_intervals() + config.history_intervals())

        # popiulate candles from excahnge
        for interval in intervals:
            self.populate_fetch_interval(
                symbol, config, current_time, candles_no, candle_events, interval, is_history)
        # generate candles from existig
        for interval in intervals_generated:
            self.populate_generated_interval(
                symbol, config, candle_events, all_intervals, interval)

        # printing things
        self.market_watch_manager.print_market_watch(symbol)
        # candle_events: list[CandleEvent] is for a perticular time for all intervals for a single symbol
        if not is_history:
            print("candle_events:", candle_events)
        return candle_events

    def populate_generated_interval(self, symbol, config, candle_events, all_intervals, interval):
        # for 1d generate from 1hr candles,so go from lower to higher, 5m-> 1hr->1d,
        # in this case vwill needed just 12 history candles for 1hr
        source_interval = market_watch_utils.get_source_interval_for_candle_generation(
            all_intervals, interval)
        source_candle_event = market_watch_utils.get_candle_event_for_interval(
            candle_events, source_interval)
        candle_event = self.market_watch_manager.generate_candles(
            symbol, source_interval, source_candle_event, interval)
        candle_events.append(candle_event)
        self.create_update_indicators(config, candle_event)

    def populate_fetch_interval(self, symbol, config, current_time, candles_no, candle_events, interval, is_history):
        candles = self.quote_service.get_candles(config.exchange(),
                                                 symbol, interval, current_time, candles_no)
        if is_history:
            candle_event = self.market_watch_manager.add_update_candles(symbol, interval,candles)
        else:                                                            
            candle_event = self.market_watch_manager.add_candles(symbol, interval,candles)
        candle_events.append(candle_event)
        self.create_update_indicators(config, candle_event)

    def create_update_indicators(self, config, candle_event):
        for indicator in config.indicators():
            self.indicator_manager.create_upadte_indicators(
                candle_event, indicator)

    def run_market_watch_scheduler(self):
        print(f"\n\n === Schedluer Triggered @ {datetime.now()} ===\n")
        self.get_current_all()
        if self.all_candle_events:
            self.event_queue.push(self.all_candle_events)

    def get_current_all(self):
        calls = []
        current_time = datetime.now()
        for symbols_config in self.engine_config.get_symbols_configs():
            for symbol in symbols_config.symbols:
                calls.append(threading.Thread(
                    target=self.get_current_symbol, args=(symbol, symbols_config.symbol_config, current_time), daemon=True))
        for call in calls:
            call.start()
        for call in calls:
            call.join()  # todo check if any thread failed by returning bool and stop
        print('Time taken to run get_current_all',
              datetime.now() - current_time)
