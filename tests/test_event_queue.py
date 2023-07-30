from queue import Queue

from src.engiene.event_queue import EventQueue


def test_queue():
    eq = EventQueue()
    eq.push(1) # type: ignore
    assert eq.pull() == 1
    # eq.push(2)
    eq.push(3) # type: ignore
    assert eq.pull() == 3