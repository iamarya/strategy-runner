from enum import Enum
from datetime import timedelta

class Duration(Enum):
    _5M = timedelta(minutes=5)
    _10M = timedelta(minutes=10)
    _1HR = timedelta(minutes=60)
    _1D = timedelta(days=1)