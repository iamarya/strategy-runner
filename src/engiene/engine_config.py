from src.models.enums import INTERVAL_TYPE

configs = {
    "backtest": False,
    "symbols": [{
        "symbol": "USDT-BTC",
        "current_intervals": [INTERVAL_TYPE.M5],
        "current_intervals_generated": [INTERVAL_TYPE.HR1, INTERVAL_TYPE.D1],
        "current_candles_no": 2,
        "history_intervals": [INTERVAL_TYPE.M5, INTERVAL_TYPE.HR1, INTERVAL_TYPE.D1],
        "history_intervals_generated": [],
        "history_candles_no": 0,
        "indicators": [],
        "type": ""
    }],
    "strategies": []
}
