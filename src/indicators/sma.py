import pandas as pd

from src.indicators.indicator import Indicator


class SMA(Indicator):
    def __init__(self, duration: int) -> None:
        super().__init__()
        self.duration = duration

    def process(self, df: pd.DataFrame, start_index: int, end_index: int):
        initial_position = start_index - \
            self.duration if start_index >= self.duration else 0
        df.iloc[start_index:end_index+1, df.columns.get_loc("sma")] = df.iloc[
            initial_position:end_index+1]["close"].rolling(self.duration).mean()[start_index-initial_position:]

    def get_columns(self) -> list[str]:
        return ["sma"]

    def get_type(self) -> str:
        return "sma"
