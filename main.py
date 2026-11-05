#!/bin/env python
import subprocess
import datetime as dt
from calendar import isleap
dates = subprocess.getoutput("git log --format='%as'").split('\n')

index = 0
for date in dates:
    dates[index] = dt.datetime.fromisoformat(date)
    index += 1

last_date = dates[0]
last_dates = []

for date in dates:
    if date.year == last_date.year:
        last_dates.append(date)
    else:
        break

last_first_day = dt.datetime.fromisoformat(str(last_date.year) + '-01-01')
last_first_weekday = last_first_day.weekday() # this is the gap at the start

today_date = dt.date.today()

week_in_days = 7
year_in_days = 366 if isleap(last_date.year) else 365

