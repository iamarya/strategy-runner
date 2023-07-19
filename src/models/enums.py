from enum import Enum
from datetime import timedelta


class Duration(Enum):
    M5 = {"time_delta": timedelta(minutes=5), "secs": 300}
    M10 = {"time_delta": timedelta(minutes=10), "secs": 600}
    HR1 = {"time_delta": timedelta(hours=1), "secs": 3600}
    D1 = {"time_delta": timedelta(days=1), "secs": 86400}
