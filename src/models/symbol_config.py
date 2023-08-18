# todo make proper model classes/ low priority
from exchange.exchange import Exchange
from indicators.indicator import Indicator
from models.enums import INTERVAL_TYPE


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