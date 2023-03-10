from unittest import TestCase

from strategy_runner.engiene.watcher import *
from strategy_runner.exchange.publisher import *
from strategy_runner.models.tick import *


class TestWatcher(TestCase):
    def test_print(self):
        publisher = TickPublisher()
        watcher = Watcher()
        publisher.subscribe(watcher)
        for i in range(3):
            publisher.emit(Tick("TCS", None, 300.50))
        watcher.print()
