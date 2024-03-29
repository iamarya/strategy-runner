from db.db import GSheetDb, InMemoryDb
from exchange.binance_exchange import BinanceExchange
from exchange.coinbase_exchange import CoinBaseExchange
from exchange.csv_exchange import CsvExchange
from exchange.mock_exchange import MockExchange
from indicators.ema import EMA
from indicators.rsi import RSI
from indicators.sma import SMA
from models.enums import DB_TYPE, EXCAHNGE_TYPE, INTERVAL_TYPE, MODE
from strategy.swing_trading_strategy import SwingTradingStrategy
from strategy.trading_view_strategy import TradingViewStrategy


# backtest means some mock exchange/ real exchange(quote) will be used and strategies will use in memory db
# and mock order service
# paper trade means strategy will use db as in memory/gsheet and mock order service
# live trade will use gsheet and actual order service
# Note: same symbol should not be setup for two different exchange until
# exchange will be part of the dict in market watch

def sample_config():
    return {
        # flag changes behaviour of engine and strategies will bound use paper trading with in memory db
        "backtest": False,
        "save_history_csv": False,
        "symbol_configs": [
            {
                # add multiple symbols here for same config
                "symbols": ["BTCUSDT"],
                "symbol_config": {
                    "current_intervals": [INTERVAL_TYPE.S5],
                    "current_intervals_generated": [],
                    "current_candles_no": 2,
                    "history_intervals": [INTERVAL_TYPE.S5],
                    "history_intervals_generated": [],
                    "history_candles_no": 0,
                    "indicators": [SMA(8), SMA(12), EMA(8), RSI(3)],
                    "exchange_type": EXCAHNGE_TYPE.MOCK_EXCAHNGE
                }
            }
        ],
        "strategy_configs": [
            {
                # will be used for backtest and paper trading
                "strategy": SwingTradingStrategy(),
                "db_type": DB_TYPE.IN_MEMORY,  # IN_MEMORY or GSHEET
                "exchange_type": EXCAHNGE_TYPE.MOCK_EXCAHNGE
            },
            # {
            #     # will be used for live trading
            #     "strategy": Strategy(),
            #     "db_type": DB_TYPE.G_SHEET,
            #     "exchange_type": EXCHANGE_TYPE.COINBASE_EXCHANGE
            # }
        ],
        "db_configs": {
            DB_TYPE.IN_MEMORY: InMemoryDb(),
            DB_TYPE.G_SHEET: GSheetDb()
        },
        "exchange_configs": {
            EXCAHNGE_TYPE.MOCK_EXCAHNGE: MockExchange(),
            EXCAHNGE_TYPE.COINBASE_EXCHANGE: CoinBaseExchange(),
            EXCAHNGE_TYPE.BINANCE_EXCAHNGE: BinanceExchange(MODE.SANDBOX)
        }
    }


def backtest_config():
    return {
        # flag changes behaviour of engine and strategies will bound use paper trading with in memory db
        "backtest": True,
        "save_history_csv": True,
        "symbol_configs": [
            {
                # add multiple symbols here for same config
                "symbols": ["BTCUSDT"],
                "symbol_config": {
                    # current settings are not processed during backtesting
                    "current_intervals": [],
                    "current_intervals_generated": [],
                    "current_candles_no": 0,
                    "history_intervals": [INTERVAL_TYPE.M15],
                    "history_intervals_generated": [],
                    "history_candles_no": 100,
                    "indicators": [SMA(9), SMA(21)],
                    "exchange_type": EXCAHNGE_TYPE.MOCK_EXCAHNGE
                }
            }
        ],
        "strategy_configs": [
            {
                # will be used for backtest and paper trading
                "strategy": SwingTradingStrategy(),
                "db_type": DB_TYPE.IN_MEMORY,  # IN_MEMORY or GSHEET
                "exchange_type": EXCAHNGE_TYPE.MOCK_EXCAHNGE
            }
        ],
        "db_configs": {
            DB_TYPE.IN_MEMORY: InMemoryDb()
        },
        "exchange_configs": {
            EXCAHNGE_TYPE.MOCK_EXCAHNGE: MockExchange(),
            EXCAHNGE_TYPE.BINANCE_EXCAHNGE: BinanceExchange(MODE.LIVE)
        }
    }


def csv_config():
    return {
        # flag changes behaviour of engine and strategies will bound use paper trading with in memory db
        "backtest": True,
        "save_history_csv": False,
        "symbol_configs": [
            {
                # add multiple symbols here for same config
                "symbols": ["BTCUSDT"],
                "symbol_config": {
                    "current_intervals": [],
                    "current_intervals_generated": [],
                    "current_candles_no": 0,
                    "history_intervals": [INTERVAL_TYPE.M15],
                    "history_intervals_generated": [],
                    "history_candles_no": 1,
                    "indicators": [SMA(9), SMA(21)],
                    "exchange_type": EXCAHNGE_TYPE.CSV_EXCHANGE
                }
            }
        ],
        "strategy_configs": [
            {
                "strategy": SwingTradingStrategy(),
                "db_type": DB_TYPE.IN_MEMORY,  # IN_MEMORY or GSHEET
                "exchange_type": EXCAHNGE_TYPE.CSV_EXCHANGE
            }
        ],
        "db_configs": {
            DB_TYPE.IN_MEMORY: InMemoryDb()
        },
        "exchange_configs": {
            EXCAHNGE_TYPE.CSV_EXCHANGE: CsvExchange(),
        }
    }


def tradingview_config():
    return {
        # flag changes behaviour of engine and strategies will bound use paper trading with in memory db
        "backtest": False,
        "save_history_csv": False,
        "symbol_configs": [
            {
                # add multiple symbols here for same config
                "symbols": ["TIME"],
                "symbol_config": {
                    "current_intervals": [INTERVAL_TYPE.S5],
                    "current_intervals_generated": [],
                    "current_candles_no": 2,
                    "history_intervals": [],
                    "history_intervals_generated": [],
                    "history_candles_no": 0,
                    "indicators": [],
                    "exchange_type": EXCAHNGE_TYPE.MOCK_EXCAHNGE
                }
            }
        ],
        "strategy_configs": [
            {
                # will be used for backtest and paper trading
                "strategy": TradingViewStrategy(),
                "db_type": DB_TYPE.IN_MEMORY,  # IN_MEMORY or GSHEET
                "exchange_type": EXCAHNGE_TYPE.MOCK_EXCAHNGE
            }
        ],
        "db_configs": {
            DB_TYPE.IN_MEMORY: InMemoryDb(),
            DB_TYPE.G_SHEET: GSheetDb()
        },
        "exchange_configs": {
            EXCAHNGE_TYPE.MOCK_EXCAHNGE: MockExchange()
        }
    }
