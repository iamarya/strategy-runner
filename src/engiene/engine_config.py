from src.models.enums import *

configs = {
    "backtest": False,  # flag changes behaviour of engine
    "symbols": [{
        "symbol": "BTC",
        "current_intervals": [INTERVAL_TYPE.S5],
        "current_intervals_generated": [INTERVAL_TYPE.HR1, INTERVAL_TYPE.D1],
        "current_candles_no": 2,
        "history_intervals": [INTERVAL_TYPE.M5, INTERVAL_TYPE.HR1, INTERVAL_TYPE.D1],
        "history_intervals_generated": [],
        "history_candles_no": 0,
        "indicators": [],
        "exchange_type": EXCAHNGE_TYPE.MOCK_EXCAHNGE
    }],
    "strategies": [{
        # will be used for backtest and paper trading
        "strategy": "S1",
        "db": DB_TYPE.IN_MEMORY,  # IN_MEMORY or GSHEET
        "exchange_type": EXCAHNGE_TYPE.MOCK_EXCAHNGE
    },
        {
            # will be used for live trading
            "strategy": "S2",
            "db": DB_TYPE.G_SHEET,
            "exchange_type": EXCAHNGE_TYPE.COINBASE_EXCHANGE
    }]
}
# backtest means some mock exchange/ real exchange(quote) will be used and strategies will be use inmemory db
# and mock order service
# papaer trade means strategy will use inmemory/gsheet and mock order serice
# live trade will use gsheet and actual order service


class SymbolConfig:
    def __init__(self, config) -> None:
        self.config = config

    def symbol(self) -> str:
        return self.config["symbol"]

    def current_intervals(self) -> list[INTERVAL_TYPE]:
        return self.config["current_intervals"]

    def current_intervals_generated(self) -> list[INTERVAL_TYPE]:
        return self.config["current_intervals_generated"]

    def current_candles_no(self) -> int:
        return self.config["current_candles_no"]

    def history_intervals(self) -> list[INTERVAL_TYPE]:
        return self.config["history_intervals"]

    def history_intervals_generated(self) -> list[INTERVAL_TYPE]:
        return self.config["history_intervals_generated"]

    def history_candles_no(self) -> int:
        return self.config["history_candles_no"]

    def indicators(self) -> list[INDICATOR_TYPE]:
        return self.config["indicators"]

    def exchange_type(self) -> EXCAHNGE_TYPE:
        return self.config["exchange_type"]


class EngineConfig:
    def __init__(self, configs) -> None:
        self.configs = configs

    def is_backtest(self) -> bool:
        return self.configs["backtest"]

    def get_all_symbols(self) -> list[str]:
        return [config["symbol"] for config in self.configs["symbols"]]

    def get_symbol_config(self, symbol) -> SymbolConfig:
        return [SymbolConfig(config) for config in self.configs["symbols"] if config["symbol"] == symbol][0]

    def get_all_configs(self) -> list[SymbolConfig]:
        return [SymbolConfig(config) for config in self.configs["symbols"]]
