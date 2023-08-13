import logging

logger = logging.getLogger(__name__)


class Record:

    def __repr__(self):
        return f'\n{self.order_type} {self.price} {self.state} {self.closed}'

    def __init__(self, symbol, order_type, price, state):
        self.row_no = None
        self.id = None
        self.parent_id = None
        self.meta_id = None
        self.symbol = symbol
        self.order_type = order_type  # buy, sell, sl
        self.created_at = None
        self.updated_at = None
        self.quantity = None
        self.price = price
        self.trigger_price = None
        self.cost = None
        self.profit = None
        self.state = state  # pending, completed, canceled, closed
        self.closed = False







class RecordBook:

    def __init__(self):
        self.data = dict()

    def add(self, strategy_name: str, strategy_records: list[Record]):
        self.data[strategy_name] = strategy_records

    def get(self, strategy_name: str) -> list[Record]:
        return self.data[strategy_name]

    def print_record_book(self):
        for symbol in self.data.keys():
            logger.info('record book for symbol: %s', symbol)
            # todo change to logging
            print(self.data.get(symbol))
