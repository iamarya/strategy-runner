class Tick:
    def __init__(self, symbol, time, price) -> None:
        self.symbol = symbol
        self.time = time
        self.price = price

    def get_time(self):
        return self.time

    def get_price(self):
        return self.price

    def get_symbol(self):
        return self.symbol
