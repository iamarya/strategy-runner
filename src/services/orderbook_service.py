from models.enums import ORDER_TYPE, STATE
from models.record_book import RecordBook, Record


class OrderBookService:

    def __init__(self, record_book: RecordBook):
        self.record_book = record_book

    def initialise_record_book(self, strategy_name: str):
        records = [] # todo get it from db
        self.record_book.add(strategy_name, records)

    # get records from db
    # if not there create inside orderbook and return
    # will be initialised during strategy register time
    def get_records(self, strategy_name: str) -> list[Record]:
        return self.record_book.get(strategy_name)

    def print_record_book(self):
        self.record_book.print_record_book()

    def buy(self, exchange, db, strategy_name:str, symbol_to_trade, buy_price):
        records = self.record_book.get(strategy_name)
        records.append(Record(symbol_to_trade, ORDER_TYPE.BUY, buy_price, STATE.BUY_CONFIRMED))

    def sell(self, exchange, db, strategy_name, symbol_to_trade, sell_price):
        records = self.record_book.get(strategy_name)
        records.append(Record(symbol_to_trade, ORDER_TYPE.SELL, sell_price, STATE.SELL_CONFIRMED))
    def mark_close(self, exchange, db, strategy_name, symbol_to_trade):
        records = self.record_book.get(strategy_name)
        for record in records:
            record.closed = True
