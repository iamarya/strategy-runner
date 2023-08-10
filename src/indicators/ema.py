import pandas as pd
from ta.trend import EMAIndicator

from indicators.indicator import Indicator


class EMA(Indicator):
    def __init__(self, window: int) -> None:
        super().__init__()
        self.window = window

    def process(self, df: pd.DataFrame, start_position: int, end_position: int):
        initial_position = start_position - \
            self.window if start_position >= self.window else 0
        df.iloc[start_position:end_position+1, df.columns.get_loc(self.get_columns()[0])] = \
            EMAIndicator(df.iloc[initial_position:end_position+1]['close'], self.window).ema_indicator()[start_position - initial_position:]

    def get_columns(self) -> list[str]:
        name = "ema_"+str(self.window)
        return [name]

    def get_type(self) -> str:
        return "ema"
