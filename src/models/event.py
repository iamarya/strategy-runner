from models.enums import EVENT_TYPE


class Event:
    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value


class CandleEvent(Event):

    def __init__(self, value) -> None:
        super().__init__(EVENT_TYPE.CANDLE_EVENT, value)


class TimerEvent(Event):

    def __init__(self, type, value) -> None:
        super().__init__(EVENT_TYPE.TIMER_EVENT, value)
