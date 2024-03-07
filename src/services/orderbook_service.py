from models.enums import TRANSACTION_TYPE, STATE
from models.record_book import RecordBook, Record


class OrderBookService:

    def __init__(self, record_book: RecordBook):
        self.record_book:RecordBook = record_book

    def initialise_record_book(self, strategy_name: str):
        records = []  # todo get it from db
        self.record_book.add(strategy_name, records)

    # get records from db
    # if not there create inside orderbook and return
    # will be initialised during strategy register time
    def get_records(self, strategy_name: str) -> list[Record]:
        return self.record_book.get(strategy_name)

    def print_record_book(self):
        self.record_book.print_record_book()

    # instead sending exchange, db, strategy name, can send the strategy itself: not now later
    def buy(self, exchange, db, strategy_name: str, symbol_to_trade, buy_price):
        id = exchange.buy_market(symbol_to_trade, 1)
        # todo use the record_book also in exchange and dont use separate order_book to hold same duplicate data
        #  think hot use same record_book and get the details and update the record_book
        #  if it will be complex then use separate order_book
        records = self.record_book.get(strategy_name)
        records.append(Record(id, symbol_to_trade, TRANSACTION_TYPE.BUY, buy_price, STATE.CONFIRMED, 'cd', 'ud', 1))

    def buy_market(self, exchange, db, strategy_name: str, symbol_to_trade, buy_price):
        # create order request
        # call buy on exchange which will return order response
        # get orderid and order creation ts and store into records
        # other methods will be sell_market, sell_sl_market
        # buy_limit, sell_limit, sell_sl_limit
        # todo question? when to update the status of order. every notify call? or separate thread? or something else?
        pass

    def sell(self, exchange, db, strategy_name, symbol_to_trade, sell_price):
        id = exchange.buy_market(symbol_to_trade, 1)
        records = self.record_book.get(strategy_name)
        records.append(Record(id, symbol_to_trade, TRANSACTION_TYPE.SELL, sell_price, STATE.CONFIRMED, 'cd', 'ud', 1))

    def mark_close(self, exchange, db, strategy_name, symbol_to_trade):
        records = self.record_book.get(strategy_name)
        for record in records:
            record.closed = True
