from src.models.enums import INTERVAL_TYPE
from src.engiene.engine_config import EngineConfig, SymbolConfig
import pandas as pd


class MarketWatch:

    def __init__(self, configs: EngineConfig) -> None:
        self.ma = dict()
        # self.configs = configs
        # setup initial ma using config
        for config in configs.get_all_configs():
            mw_item = dict()
            columns = ['time', 'open', 'high', 'low', 'close', 'volume']
            df = pd.DataFrame(columns=columns, index=range(100))
            mw_item[INTERVAL_TYPE.M5] = df
            self.ma[config.symbol()] = mw_item

    def get_ltp(self, symbol: str) -> float:
        return self.ma[symbol].ltp

    def get_chart(self, symbol: str, inetval: INTERVAL_TYPE):
        return self.ma[symbol].interval

    def get_last_updated(self, symbol: str):
        return self.ma[symbol].last_updated_time


'''
Example:
{
    "ETH": {
        "symbol": "ETH",
        M5: None: DataFrame,
        D1: None,
        "indicators": [i1, i2], #may be not needed
        "ltp": 123,
        "last_updated_time": 12222987654
        "length": 10
    }
}

'''
