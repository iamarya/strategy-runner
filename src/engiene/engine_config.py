from src.models.enums import INTERVAL_ENUM

configs = {
    "symbols": [{
        "symbol": "USDT-BTC",
        "current_intervals": [INTERVAL_ENUM.M5],
        "current_intervals_generated": [INTERVAL_ENUM.HR1, INTERVAL_ENUM.D1],
        "current_candles": 2,
        "history_intervals": [INTERVAL_ENUM.M5, INTERVAL_ENUM.HR1, INTERVAL_ENUM.D1],
        "history_intervals_generated": [],
        "history_candles": 0,
        "indicators": [],
        "type": ""
    }],
    "strategies": []
}
