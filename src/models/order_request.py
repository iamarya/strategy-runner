"""Module providing a function printing python version."""
from dataclasses import dataclass

@dataclass
class OrderRequest:
    """Class representing a person"""

    def __init__(self, quantity, price, order_type, transaction_type, trigger_price):
        """Class representing a __init__"""
        self.quantity = quantity
        self.price = price
        self.order_type = order_type
        self.transaction_type = transaction_type
        self.trigger_price = trigger_price



