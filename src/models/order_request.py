class OrderRequest:
    def __int__(self, quantity, price, order_type, transaction_type, trigger_price):
        self.quantity = quantity
        self.price = price
        self.order_type = order_type
        self.transaction_type = transaction_type
        self.trigger_price = trigger_price



