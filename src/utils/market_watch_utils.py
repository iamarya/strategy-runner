
from models.candle_update_detail import CandleUpdateDetail
from models.enums import INTERVAL_TYPE


def get_source_interval_for_candle_generation(
        all_intervals: list[INTERVAL_TYPE], target_interval: INTERVAL_TYPE) -> INTERVAL_TYPE:
    found = False
    for item in reversed(INTERVAL_TYPE):
        if item == target_interval:
            found = True
            continue
        if found == True and all_intervals.count(item) > 0:
            return item
    raise ValueError(
        "get_source_interval_for_candle_generation", target_interval)


def get_candle_update_detail_for_interval(candle_update_details: list[CandleUpdateDetail], source_interval: INTERVAL_TYPE) -> CandleUpdateDetail:
    for cud in candle_update_details:
        if cud.interval == source_interval:
            return cud
    raise ValueError("get_candle_update_detail_for_interval",
                     candle_update_details, source_interval)
