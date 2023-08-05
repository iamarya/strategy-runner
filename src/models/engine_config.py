from exchange.exchange import Exchange
from strategy.strategy import Strategy
from models.enums import *
from indicators.indicator import Indicator


# todo make proper model classes/ low priority
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

    def is_save_history_csv(self) -> bool:
        return self.engine_config['save_history_csv']

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
