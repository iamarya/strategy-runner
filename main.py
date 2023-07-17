from flask import Flask
from src.engiene.engine import Engine

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Trading Bot!'

# main driver function
if __name__ == '__main__':
    engine = Engine()
    engine.start()
    app.run()