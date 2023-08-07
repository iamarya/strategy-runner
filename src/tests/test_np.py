import numpy as np


def test_np():
    print(3 > np.nan)  # False
    print(type(np.nan))  # float
    print(np.isnan(np.nan))  # True
    nd = np.array([1, 2, np.nan])
    print(np.isnan(nd).any()) # True
    print(np.isnan(nd).all()) # False
    print(type(nd[0]))
    print(np.isnan([nd[0], nd[1], nd[2]]).any())
