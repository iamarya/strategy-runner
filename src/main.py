from flask import Flask

from config import log_configs
from models.engine_config import EngineConfig
from engine.engine import Engine
import config.engine_configs as configs

app = Flask(__name__)


@app.route('/')
def hello():
    return '└|∵|┘'


# main driver function
if __name__ == '__main__':
    print('└[∵┌]└[ ∵ ]┘[┐∵]┘')
    log_configs.setup()
    # choose which config to use
    engine_config = EngineConfig(configs.csv_config())
    engine = Engine(engine_config)
    engine.start()
    if not engine_config.is_backtest():
        app.run()
    else:
        engine.join()
