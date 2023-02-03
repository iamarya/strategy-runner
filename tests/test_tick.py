from unittest import TestCase

from strategy_runner.models.tick import Tick


class TestTick(TestCase):
    def test_get(self):
        tick = Tick("TCS", None, 300.50)
        assert tick.get_symbol() == "TCS"
