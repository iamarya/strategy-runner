import unittest
import datetime as dt
import logging


curr = dt.datetime.now()
ts = curr.timestamp()
di=int(ts/(24*60*60))*(24*60*60)
print(di)
bc=dt.datetime.fromtimestamp(di)
print(curr, bc)
print(dt.datetime.fromtimestamp(0))
print(dt.datetime.fromtimestamp(1000*24*60*60))
print(bc.utcnow())