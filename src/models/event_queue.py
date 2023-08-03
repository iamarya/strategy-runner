from queue import Queue

from models.candle_update_detail import CandleUpdateDetail
from models.event import Event


class EventQueue:
    def __init__(self) -> None:
        self.q = Queue(maxsize=1)

    # its blocking
    def push(self, event: Event):
        # no time out is configured for now
        self.q.put(event, block=True)

    # return the event, non blocking
    def pull(self) -> Event|None:
        try:
            return self.q.get_nowait()  # may raise Empty exception.
        except:
            return None
