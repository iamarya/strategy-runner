class RecordBook:

    def __int__(self):
        self.data = dict(str, list(Record))

    def initialise(self):
        pass


class Record:

    def __int__(self):
        self.row_no = None
        self.id = None
        self.parent_id = None
        self.meta_id = None
        self.symbol = None
        self.type = None  # buy, sell, sl
        self.created_at = None
        self.updated_at = None
        self.quantity = None
        self.price = None
        self.trigger_price = None
        self.cost = None
        self.profit = None
        self.status = None  # pending, completed, canceled, closed
