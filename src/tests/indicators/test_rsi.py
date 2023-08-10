import numpy as np
import pandas as pd
from ta.momentum import RSIIndicator
from indicators.rsi import RSI


def test_rsi():
    '''
1691652360    8    2   9     4    100   NaN    NaN   NaN        NaN
1691652365    4    3   3     6    100   NaN    NaN   NaN        NaN
1691652370    6   10   1     6    100   NaN    NaN   NaN      100.0
1691652375    7   10   5     5    100   NaN    NaN   NaN  47.058824
1691652380    3    2   2     9    100   NaN    NaN   NaN  87.323944
    '''
    arr = np.array([4,6,6,5,9])
    se=pd.Series(arr)

    r = RSIIndicator(se, 3).rsi()
    print(r)