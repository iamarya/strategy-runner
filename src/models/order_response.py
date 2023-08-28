class OrderResponse:
    def __int__(self, order_id, status=None, average_price=None, order_created=None, order_updated=None):
        self.order_id = order_id
        self.status = status
        self.average_price = average_price
        self.order_created = order_created
        self.order_updated = order_updated
