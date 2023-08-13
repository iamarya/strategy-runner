import logging
from exchange.mock_exchange import MockExchange
from models.candle import Candle
from models.enums import INTERVAL_TYPE
import csv

logger = logging.getLogger(__name__)


def get_csv_file(symbol, interval):
    file = None
    if symbol == 'BTCUSDT' and interval == INTERVAL_TYPE.M15:
        file = '../tmp/BTCUSDT_M15_1yr_binace.csv'
    elif symbol == 'BTCUSDT' and interval == INTERVAL_TYPE.M5:
        file = '../tmp/BTCUSDT_M5-2yr.csv'
    logger.info('File used is %s', file)
    return file


class CsvExchange(MockExchange):

    def is_live(self) -> bool:
        return False
    
    def get_candles(self, symbol: str, interval: INTERVAL_TYPE, from_time: int, to_time: int) -> list[Candle]:
        candles = []
        csv_file = get_csv_file(symbol, interval)
        if csv_file is None:
            return []
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                if row[0] == 'time':
                    continue
                candles.append(Candle(int(row[0]), float(row[1]), float(row[2]), float(row[3]),
                                      float(row[4]), float(row[5])))
        return candles


if __name__ == '__main__':
    li = CsvExchange().get_candles('BTCUSDT', INTERVAL_TYPE.M5, 0, 0)
    print(len(li))
