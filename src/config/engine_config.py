from db.db import GSheetDb, InMemoryDb
from exchange.exchange import CoinBaseExchange, Exchange, MockExchange
from strategy.strategy import Strategy
from strategy.swing_trading_strategy import SwingTradingStrategy
from models.enums import *
from indicators.sma import SMA
from indicators.indicator import Indicator

sample_config = {
    # flag changes behaviour of engine and strategies will bound use paper trading with inmeroy db
    "backtest": False,
    "symbol_configs": [
        {
            # add multiple symbools here for same config
            "symbols": ["BTC"],
            "symbol_config":  {
                "current_intervals": [INTERVAL_TYPE.S5],
                "current_intervals_generated": [INTERVAL_TYPE.HR1, INTERVAL_TYPE.D1],
                "current_candles_no": 2,
                "history_intervals": [INTERVAL_TYPE.S5, INTERVAL_TYPE.HR1, INTERVAL_TYPE.D1],
                "history_intervals_generated": [],
                "history_candles_no": 3,
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
        EXCAHNGE_TYPE.COINBASE_EXCHANGE: CoinBaseExchange()
    }
}

# backtest means some mock exchange/ real exchange(quote) will be used and strategies will be use inmemory db
# and mock order service
# papaer trade means strategy will use db as inmemory/gsheet and mock order serice
# live trade will use gsheet and actual order service


class SymbolConfig:
    def __init__(self, symbol_config, exchange_config) -> None:
        self.symbol_config = symbol_config
        self.exchange_config = exchange_config

    def current_intervals(self) -> list[INTERVAL_TYPE]:
        return self.symbol_config["current_intervals"]

    def current_intervals_generated(self) -> list[INTERVAL_TYPE]:
        return self.symbol_config["current_intervals_generated"]

    def current_candles_no(self) -> int:
        return self.symbol_config["current_candles_no"]

    def history_intervals(self) -> list[INTERVAL_TYPE]:
        return self.symbol_config["history_intervals"]

    def history_intervals_generated(self) -> list[INTERVAL_TYPE]:
        return self.symbol_config["history_intervals_generated"]

    def history_candles_no(self) -> int:
        return self.symbol_config["history_candles_no"]

    def indicators(self) -> list[Indicator]:
        return self.symbol_config["indicators"]

    def exchange(self) -> Exchange:
        return self.exchange_config[self.symbol_config["exchange_type"]]


class SymbolsConfig:
    def __init__(self, symbols: list[str], symbol_config: SymbolConfig) -> None:
        self.symbols = symbols
        self.symbol_config = symbol_config


class EngineConfig:
    def __init__(self, engine_config) -> None:
        self.engine_config = engine_config

    def is_backtest(self) -> bool:
        return self.engine_config["backtest"]

    # def get_all_symbols(self) -> list[str]:
    #     return []
    #     # return [config["symbol"] for config in self.engine_config["symbols"]]

    def get_symbols_configs(self) -> list[SymbolsConfig]:
        symbols_configs = []
        for config in self.engine_config["symbol_configs"]:
            symbols_config = SymbolsConfig(config["symbols"], SymbolConfig(
                config["symbol_config"], self.engine_config['exchange_configs']))
            symbols_configs.append(symbols_config)
        return symbols_configs

    def get_strategies(self) -> list[Strategy]:
        strategies: list[Strategy] = []
        for config in self.engine_config["strategy_configs"]:
            strategy = config['strategy']
            db = self.engine_config['db_configs'][config['db_type']]
            exchange = self.engine_config['exchange_configs'][config['exchange_type']]
            strategy.set_db(db)
            strategy.set_exchange(exchange)
            strategies.append(strategy)
        return strategies
