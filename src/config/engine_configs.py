from db.db import GSheetDb, InMemoryDb
from exchange.binance_exchange import BinanceExchange
from exchange.coinbase_exchange import CoinBaseExchange
from exchange.mock_exchange import MockExchange
from indicators.sma import SMA
from models.enums import DB_TYPE, EXCAHNGE_TYPE, INTERVAL_TYPE, MODE
from strategy.swing_trading_strategy import SwingTradingStrategy


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
                    "history_candles_no": 13,
                    "indicators": [SMA(8), SMA(13)],
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
        "save_history_csv": False,
        "symbol_configs": [
            {
                # add multiple symbols here for same config
                "symbols": ["BTCUSDT"],
                "symbol_config": {
                    "current_intervals": [],
                    "current_intervals_generated": [],
                    "current_candles_no": 0,
                    "history_intervals": [INTERVAL_TYPE.M5],
                    "history_intervals_generated": [],
                    "history_candles_no": 1000,
                    "indicators": [SMA(8), SMA(13)],
                    "exchange_type": EXCAHNGE_TYPE.BINANCE_EXCAHNGE
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

# backtest means some mock exchange/ real exchange(quote) will be used and strategies will use in memory db
# and mock order service
# paper trade means strategy will use db as in memory/gsheet and mock order service
# live trade will use gsheet and actual order service
