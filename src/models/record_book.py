import logging

logger = logging.getLogger(__name__)


class Record:

    def __repr__(self):
        return f'\n{self.order_type} {self.price} {self.state} {self.closed}'

    def __init__(self, id, symbol, transaction_type, order_type, state, created_at, updated_at, quantity,
                 row_no=None, parent_id=None, meta_id=None, price=None, limit_price=None, trigger_price=None,
                 cost=None, profit=None):
        self.row_no = row_no
        self.id = id
        self.parent_id = parent_id
        self.meta_id = meta_id
        self.symbol = symbol
        self.transaction_type = transaction_type # buy, sell, sl
        self.order_type = order_type  # market, limit, sl-market, sl_limit
        self.created_at = created_at
        self.updated_at = updated_at
        self.quantity = quantity
        self.price = price # actual order executed price
        self.limit_price = limit_price # limit price
        self.trigger_price = trigger_price
        self.cost = cost
        self.profit = profit
        self.state = state  # pending, completed, canceled
        self.closed = False


class RecordBook:

    def __init__(self):
        self.data = dict()

    def add(self, strategy_name: str, strategy_records: list[Record]):
        self.data[strategy_name] = strategy_records

    def get(self, strategy_name: str) -> list[Record]:
        return self.data[strategy_name]

    def print_record_book(self):
        for strategy in self.data.keys():
            logger.info('record book for symbol: %s', strategy)
            # todo change to logging
            print(self.data.get(strategy))
