import datetime as dt
import math

# use Python 3.10.12 to reproduce
# def test_exchange_start_at_different_time():
#     # genric formula
#     # start_time = dt.datetime.fromisoformat('2023-07-25T03:45:00Z')
#     start_time = dt.datetime.fromisoformat('2023-07-25T03:45:00 +0000')
#     print(start_time)
#     # 3:45 utc kite starts
#     offset = dt.timedelta(hours=3, minutes=45)
#     print("given time:", start_time)
#     indicator = 24*60*60
#     day_secs = (24*60*60)

#     # print((start_time- offset).timestamp()/day_secs) -- 19563.0
#     complete_days = math.floor((start_time- offset).timestamp()/day_secs)
#     # extra_secs= start_time.timestamp()%(complete_days*day_secs)
#     extra_secs = (start_time- offset).timestamp()%day_secs
#     print(extra_secs)
#     indi_start_day_sec = math.floor(extra_secs/indicator)*indicator
#     indi_start_sec = (complete_days*day_secs)+offset.total_seconds() + indi_start_day_sec
#     indi_start_dt = dt.datetime.utcfromtimestamp(indi_start_sec)
#     print("indicator start time:", indi_start_dt)
#     assert 1 == 1