<h1 align="center">
  <br>
  <img src="https://github.com/iamarya/strategy-runner/blob/main/.github/bot.png?raw=true" alt="" width="200">
  <br>
  STRATEGY RUNNER
</h1>

<h4 align="center">This is a trading bot where you can do back testing, papaer trading and live tradings.</h4>

## Features
- Backtesting
- Papaer trading
- Live trading

## ToDo
- Safeguards, ex: engine config validation, safe exit, shutdown hook, error handling (mainly in strategiy, also for market data)
- Two type of strategy, 
  - one depends on candle event, which can be backtested
  - other type depends cant be backtested depends on timely triggered.
- evaluation of strategy: not just total return also add risk, volatility, drawdown => sharp ratio
- logging framework
- unit test cases 
- Priority wise:
  - backtest
    - kite/ coinbase for market data intigration
    - backtest (candle event synthsize)
    - backtest (save as csv)
    - simple strategy
    - db (inmemory)
    - simple report from db
  - ml resarch
  - paper trading
    - mock order service
  - gsheet integration (db)

  

## License
>You can check out the full license [here](https://github.com/iamarya/strategy-runner/blob/master/LICENSE)
