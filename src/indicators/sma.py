import pandas as pd

from indicators.indicator import Indicator


class SMA(Indicator):
    def __init__(self, duration: int) -> None:
        super().__init__()
        self.duration = duration

    def process(self, df: pd.DataFrame, start_position: int, end_position: int):
        initial_position = start_position - \
            self.duration if start_position >= self.duration else 0
        df.iloc[start_position:end_position+1, df.columns.get_loc("sma")] = df.iloc[
            initial_position:end_position+1]["close"].rolling(self.duration).mean()[start_position-initial_position:]

    def get_columns(self) -> list[str]:
        return ["sma"]

    def get_type(self) -> str:
        return "sma"
