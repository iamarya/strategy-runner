from unittest import TestCase

from src.models.candle import Candle


class TestTick(TestCase):
    def test_get(self):
        candle = Candle(None, 12, 5, 7, 9, 100)
        assert candle.h == 12
