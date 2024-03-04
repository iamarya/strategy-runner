from queue import Queue

from models.event import Event


class EventQueue:
    def __init__(self) -> None:
        self.q = Queue(maxsize=1)

    # its blocking
    def push(self, event: Event):
        # no time out is configured for now
        self.q.put(event, block=True)

    # return the event, non-blocking
    # update: changed to blocking as there will be no strategy run if no event. 
    #   earlier it was needed as if no candle event, still may need to run strategy for timmer.
    def pull(self) -> Event|None: 
        # block until get an event
        return self.q.get()  # changed form get_nowait which raise Empty exception.
