from src.models.enums import Duration

configs = {
    "symbols": [{
        "symbol": "USDT-BTC",
        "current_intervals": [Duration.M5],
        "current_intervals_generated": [Duration.HR1, Duration.D1],
        "current_candles": 2,
        "history_intervals": [Duration.M5, Duration.HR1, Duration.D1],
        "history_intervals_generated": [],
        "history_candles": 0,
        "indicators": [],
        "type": ""
    }],
    "strategies": []
}
