<h1 align="center">
  <br>
  <img src="https://github.com/iamarya/strategy-runner/blob/main/.github/bot.png?raw=true" alt="" width="200">
  <br>
  STRATEGY RUNNER
</h1>

<h4 align="center">This is a trading bot where you can do back test as well.</h4>

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
  

## License
>You can check out the full license [here](https://github.com/iamarya/strategy-runner/blob/master/LICENSE)
