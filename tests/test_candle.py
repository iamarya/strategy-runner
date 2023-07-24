import pytest
from src.models.candle import Candle
from collections import namedtuple

CandlePair = namedtuple('CandlePair', 'c1 c2')

@pytest.fixture
def get_candle()-> CandlePair:    
    return CandlePair(Candle(123, 12, 5, 7, 9, 100), Candle(124, 12, 5, 7, 9, 100))

def test_get(get_candle:CandlePair):
    assert get_candle.c1.h == 5

def test_get2(get_candle):
    assert get_candle.c2.c == 9