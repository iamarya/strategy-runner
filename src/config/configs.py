from db.db import GSheetDb, InMemoryDb
from exchange.coinbase_exchange import CoinBaseExchange
from exchange.binance_exchange import BinanceExchange
from exchange.mock_exchange import MockExchange
from indicators.sma import SMA
from models.enums import DB_TYPE, EXCAHNGE_TYPE, INTERVAL_TYPE
from strategy.swing_trading_strategy import SwingTradingStrategy

sample_config = {
    # flag changes behaviour of engine and strategies will bound use paper trading with inmeroy db
    "backtest": False,
    "save_history_csv": False,
    "symbol_configs": [
        {
            # add multiple symbools here for same config
            "symbols": ["BTC"],
            "symbol_config": {
                "current_intervals": [INTERVAL_TYPE.S5],
                "current_intervals_generated": [INTERVAL_TYPE.HR1, INTERVAL_TYPE.D1],
                "current_candles_no": 2,
                "history_intervals": [INTERVAL_TYPE.S5, INTERVAL_TYPE.HR1, INTERVAL_TYPE.D1],
                "history_intervals_generated": [],
                "history_candles_no": 5,
                "indicators": [SMA(5)],
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
        #     "exchange_type": EXCAHNGE_TYPE.COINBASE_EXCHANGE
        # }
    ],
    "db_configs": {
        DB_TYPE.IN_MEMORY: InMemoryDb(),
        DB_TYPE.G_SHEET: GSheetDb()
    },
    "exchange_configs": {
        EXCAHNGE_TYPE.MOCK_EXCAHNGE: MockExchange(),
        EXCAHNGE_TYPE.COINBASE_EXCHANGE: CoinBaseExchange(),
        EXCAHNGE_TYPE.BINANCE_EXCAHNGE: BinanceExchange()
    }
}

# backtest means some mock exchange/ real exchange(quote) will be used and strategies will be use inmemory db
# and mock order service
# papaer trade means strategy will use db as inmemory/gsheet and mock order serice
# live trade will use gsheet and actual order service
