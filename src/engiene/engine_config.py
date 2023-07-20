from src.models.enums import INTERVAL_TYPE, EXCAHNGE_TYPE

configs = {
    "backtest": False, # flag changes behaviour of engine
    "symbols": [{
        "symbol": "BTC",
        "current_intervals": [INTERVAL_TYPE.M5],
        "current_intervals_generated": [INTERVAL_TYPE.HR1, INTERVAL_TYPE.D1],
        "current_candles_no": 2,
        "history_intervals": [INTERVAL_TYPE.M5, INTERVAL_TYPE.HR1, INTERVAL_TYPE.D1],
        "history_intervals_generated": [],
        "history_candles_no": 0,
        "indicators": [],
        "exchange_type": EXCAHNGE_TYPE.MOCK_EXCAHNGE
    }],
    "strategies": [{
            # will be used for backtest and paper trading
            "strategy": "S1",
            "db": IN_MEMORY, #IN_MEMORY or GSHEET
            "exchange_type": EXCAHNGE_TYPE.MOCK_EXCAHNGE
        },
        {
            # will be used for live trading
            "strategy": "S2",
            "db": GSHEET,
            "exchange_type": EXCAHNGE_TYPE.COINBASE_EXCHANGE
        }]
}
# backtest means some mock exchange/ real exchange(quote) will be used and strategies will be use inmemory db and mock order service
# papaer trade means strategy will use inmemory/gsheet and mock order serice
# live trade will use gsheet and actual order service