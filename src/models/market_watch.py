from src.models.enums import INTERVAL_TYPE
from src.engiene.engine_config import EngineConfig, SymbolConfig

class MarketWatch:
    def __init__(self, configs:EngineConfig) -> None:
        self.ma = dict()
        self.configs = configs
        # setup initial ma using config
    
    def get_ltp(self, symbol:str) -> float:
        return self.ma[symbol].ltp
    
    def get_chart(self, symbol:str, inetval: INTERVAL_TYPE):
        return self.ma[symbol].interval
    
    def get_last_updated(self, symbol:str):
        return self.ma[symbol].last_updated_time 

'''
Example:
{
    "ETH": {
        "M5": None: DataFrame,
        "D1": None,
        "indicators": [i1, i2], #may be not needed
        "ltp": 123,
        "last_updated_time": 12222987654
    }
}

'''