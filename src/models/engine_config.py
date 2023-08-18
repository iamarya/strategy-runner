from exchange.exchange import Exchange
from exchange.mock_exchange import MockExchange
from models.symbol_config import SymbolsConfig, SymbolConfig
from strategy.strategy import Strategy
from models.enums import *


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

    def get_mock_exchanges(self) -> list[MockExchange]:
        return [v for k, v in self.engine_config['exchange_configs'].items() if k == EXCAHNGE_TYPE.MOCK_EXCAHNGE
                or k == EXCAHNGE_TYPE.CSV_EXCHANGE]
