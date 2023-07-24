from unittest import TestCase

from src.models.candle import Candle


class TestCandle(TestCase):
    def test_get(self):
        candle = Candle(123, 12, 5, 7, 9, 100)
        assert candle.h == 5
