import pandas as pd
from ta.momentum import RSIIndicator

from indicators.indicator import Indicator


class RSI(Indicator):
    def __init__(self, window: int) -> None:
        super().__init__()
        self.window = window

    def process(self, df: pd.DataFrame, start_position: int, end_position: int):
        initial_position = start_position - \
            self.window if start_position >= self.window else 0
        df.iloc[start_position:end_position+1, df.columns.get_loc(self.get_columns()[0])] = \
            RSIIndicator(df.iloc[initial_position:end_position+1]['close'], self.window).rsi()[start_position-initial_position:]

    def get_columns(self) -> list[str]:
        name = "rsi_"+str(self.window)
        return [name]

    def get_type(self) -> str:
        return "rsi"
