from abc import abstractmethod
import pandas as pd


class Indicator:

    @abstractmethod
    def process(self, df: pd.DataFrame, start_position: int, end_position: int):
        pass

    @abstractmethod
    def get_type(self) -> str:
        return ""

    @abstractmethod
    def get_columns(self) -> list[str]:
        return []
