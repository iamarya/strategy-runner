from unittest import TestCase

from src.engiene.engine import *
from src.exchange.quote_service import *
from src.models.tick import *


class TestWatcher(TestCase):
    def test_print(self):
        publisher = TickPublisher()
        watcher = Watcher()
        publisher.subscribe(watcher)
        for i in range(3):
            publisher.emit(Tick("TCS", None, 300.50))
        watcher.print()
