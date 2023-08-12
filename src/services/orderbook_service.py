from models.record_book import RecordBook, Record


class OrderBookService:

    def __init__(self, order_book: RecordBook):
        self.order_book = order_book

    # get records from db
    # if not there create inside orderbook and return
    # will be initialised during strategy register time
    def get_records(self, strategy_name: str) -> list[Record]:
        return []
