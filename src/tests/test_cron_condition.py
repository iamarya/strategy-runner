import croniter
import datetime

now = datetime.datetime.now()
sched = '* 15 * * *'    # at 3:01pm on the 1st and 15th of every month
cron = croniter.croniter(sched, now)

# for i in range(4):
#     nextdate = cron.get_next(datetime.datetime)
#     print(nextdate)

crontime = cron.get_prev(datetime.datetime)
if now-crontime < datetime.timedelta(seconds=10):
    print('matching cron')
else:
    print('not matching')
