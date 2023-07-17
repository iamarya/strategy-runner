from datetime import datetime

class Candle:

    def __init__(self, t:datetime, h:float, l:float, o:float, c:float, v:int) -> None:
        self.t = t
        self.h = h
        self.l = l
        self.o = o
        self.c = c
        self.v = v