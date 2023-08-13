class Candle:

    def __init__(self, t: int, o: float, h: float, l: float, c: float, v: float) -> None:
        self.t = t # in secs of the start of teh duration
        self.h = h
        self.l = l
        self.o = o
        self.c = c
        self.v = v

    def __repr__(self) -> str:
        return str([self.t, self.o, self.h, self.l, self.c, self.v])
