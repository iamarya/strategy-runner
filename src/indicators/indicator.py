import pandas as pd


class Indicator:
    def process(self, df: pd.DataFrame, start_index: int, end_index: int):
        pass

    def get_type(self) -> str:
        return ""
    
    def get_columns(self) -> list[str]:
        return []
