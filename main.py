from flask import Flask
from src.engiene.engine import Engine
from src.engiene.engine_config import engine_config

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Trading Bot!'

# main driver function
if __name__ == '__main__':
    engine = Engine(engine_config)
    engine.start()
    app.run()