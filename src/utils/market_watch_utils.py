

from src.models.event import CandleEvent
from src.models.enums import INTERVAL_TYPE


def get_source_interval_for_candle_generation(
        current_intervals:list[INTERVAL_TYPE], target_interval:INTERVAL_TYPE)-> INTERVAL_TYPE:
    found = False
    for item in reversed(INTERVAL_TYPE):
        if item == target_interval:
            found=True
        if found == True and current_intervals.count(item) > 0:
            return item
    raise ValueError("get_source_interval_for_candle_generation")

def get_candle_event_for_interval(candle_events: list[CandleEvent], source_interval:INTERVAL_TYPE)-> CandleEvent:
    for ce in candle_events:
        if ce.interval == source_interval:
            return ce
    raise ValueError("get_candle_event_for_interval")
