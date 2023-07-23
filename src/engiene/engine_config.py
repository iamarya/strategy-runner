from src.strategy.swing_trading_strategy import SwingTradingStrategy
from src.models.enums import *
from src.indicators.sma import SMA
from src.indicators.indicator import Indicator

engine_config = {
    "backtest": False,  # flag changes behaviour of engine
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
                "history_candles_no": 10,
                "indicators": [SMA(5)],
                "exchange_type": EXCAHNGE_TYPE.MOCK_EXCAHNGE
            }
        }
    ],
    "strategies": [
        {
            # will be used for backtest and paper trading
            "strategy": "S1",
            "db": DB_TYPE.IN_MEMORY,  # IN_MEMORY or GSHEET
            "exchange_type": EXCAHNGE_TYPE.MOCK_EXCAHNGE
        },
        {
            # will be used for live trading
            "strategy": SwingTradingStrategy(),
            "db": DB_TYPE.G_SHEET,
            "exchange_type": EXCAHNGE_TYPE.COINBASE_EXCHANGE
        }
    ]
}

# backtest means some mock exchange/ real exchange(quote) will be used and strategies will be use inmemory db
# and mock order service
# papaer trade means strategy will use db as inmemory/gsheet and mock order serice
# live trade will use gsheet and actual order service


class SymbolConfig:
    def __init__(self, symbol_config) -> None:
        self.symbol_config = symbol_config

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

    def exchange_type(self) -> EXCAHNGE_TYPE:
        return self.symbol_config["exchange_type"]


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

    def get_all_configs(self) -> list[SymbolsConfig]:
        return [SymbolsConfig(config["symbols"], SymbolConfig(config["symbol_config"])) for config in self.engine_config["symbol_configs"]]
