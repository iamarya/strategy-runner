from flask import Flask
from config.engine_config import EngineConfig
from engiene.engine import Engine
import config.configs as configs

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Trading Bot!'

# main driver function
if __name__ == '__main__':
    # chhose which config to use
    engine_config = EngineConfig(configs.sample_config)
    engine = Engine(engine_config)
    engine.start()
    if engine_config.is_backtest() == False:
        app.run()
    else:
        engine.join()