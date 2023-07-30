from flask import Flask
from src.engiene.engine import Engine
import src.engiene.engine_config as ec

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Trading Bot!'

# main driver function
if __name__ == '__main__':
    # chhose which config to use
    engine_config = ec.EngineConfig(ec.sample_config)
    engine = Engine(engine_config)
    engine.start()
    if engine_config.is_backtest() == False:
        app.run()
    else:
        engine.join()