from enum import Enum
from datetime import timedelta


class Duration(Enum):
    M5 = timedelta(minutes=5)
    M10 = timedelta(minutes=10)
    HR1 = timedelta(minutes=60)
    D1 = timedelta(days=1)
