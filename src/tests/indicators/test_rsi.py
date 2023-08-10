import numpy as np
import pandas as pd
from ta.momentum import RSIIndicator
from indicators.rsi import RSI


def test_rsi():
    arr = np.array([1,2,1,4,5,6])
    se=pd.Series(arr)

    r = RSIIndicator(se, 3).rsi()
    print(r)