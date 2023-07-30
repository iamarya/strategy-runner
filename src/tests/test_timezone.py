import datetime
import pytz

utc_now = pytz.utc.localize(datetime.datetime.utcnow())

print(datetime.datetime.utcnow())
print(utc_now)