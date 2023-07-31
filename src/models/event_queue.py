from queue import Queue

from models.event import CandleEvent


class EventQueue:
    def __init__(self) -> None:
        self.q = Queue(maxsize=1)

    # its blocking
    def push(self, event: dict[str, list[CandleEvent]]):
        # no time out is configured for now
        self.q.put(event, block=True)

    # return the event, non blocking
    def pull(self) -> dict[str, list[CandleEvent]]:
        try:
            return self.q.get_nowait()  # may raise Empty exception.
        except:
            return {}
