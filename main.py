#!/bin/env python
import argparse
import subprocess # For running git (we need to dipose this later, to make the program extensible)
import datetime as dt # For all date operations
from calendar import isleap, monthrange # To decide whether a given year has 366 or 365 days
from operator import itemgetter # To sort the coordinates
#from itertools import cycle # To combine lists
from enum import Enum

parser = argparse.ArgumentParser (
    prog = 'california',
    description = 'Github style grid calendar, now available in your CLI!',
    epilog = 'Submit your own plugins to: https://github.com/rust-Iang/california/'
)
parser.add_argument('-l', '--last', action='store_true')
parser.add_argument('-d', '--date', type=str)
args = parser.parse_args()

DAYS_PER_WEEK = 7
DAYS_PER_YEAR = 365
WEEKS = 53 # CODEBERG HAS 54
SUNDAY = 6
COL = 0
ROW = 1
STEP = dt.timedelta(1)
WEEKDAYS = ('Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat')
##MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
MONTHS = ('J', 'F', 'M', 'A', 'm', 'J', 'j', 'a', 'S', 'O', 'N', 'D')  
events = subprocess.getoutput("git log --format='%as'").split('\n')
for i, event in enumerate(events):
    '''
        Converts the events from str to a datetime object.
        Useful for having access to class attributes/methods such as:
            .year, .month, .day and .weekday()
        and simple arithmetic operations while retaining a string repr.
    '''
    events[i] = dt.datetime.fromisoformat(event)

# We need to add something that always sorts the subprocess output to
# descendant order (newest first), so that events[0] is always the most
# recent date in the list.
#
# Decide whether to use dt.datetime.now() or dt.date.today():
#     if event >= start_date:
#   TypeError: can't compare datetime.datetime to datetime.date
#
# Special emphasis is brought to the following line, for we might
# explicitly format the string in all parts of the document, to make it
# more intuitive to contributors. We have e a problem here, for we
# might want to represent the dates with hours, minutes, seconds, but
# we shouldn't compare full days using them (for we would be comparing
# only a fraction of the whole day).

try: final_date = events[0] if args.last else dt.datetime.fromisoformat(args.date) if args.date else dt.datetime.now()
except ValueError:
    print('The date you have typed might not exist at all, try with another date.')
    exit()

print('original date:', final_date)
final_date = final_date.replace(hour=0, minute=0, second=0, microsecond=0) # THERE IS A PROBLEMWITH THIS, WE SHOULDNT BE GETTING 371 RANGE NUMBERS
final_date += STEP
##final_date += dt.timedelta(1)
# The following is the block used to set the start_date variable:
try:
    # Can we make it self aware of the variable we are replacing?
    # Like sys.argv[0]?
    start_date = final_date.replace(year=final_date.year - 1, day=final_date.day)
    ##start_date = final_date - dt.timedelta(DAYS_PER_YEAR + (week - weekday ))
except ValueError: # This is for leap years
    start_date = final_date.replace(year=final_date.year - 1, day=final_date.day + 1)
else:
    '''
        Github grid's first row is Sunday.
        If it the start_date variable isn't already one, then substract
        the current weekday number + 1 to achieve it.

        No, there's no point in using isoweekday() because then we
        would have to do 'SUNDAY - 1', so it's basically the same.
    '''
    if (weekday := start_date.weekday()) != SUNDAY:
        start_date -= dt.timedelta(weekday + 1)

print(final_date - start_date)

latest_events = []
for event in events:
    '''
        Selects just the latest event dates to operate on.

        In Github, the whole contribution grid is 53*7 (371), that is
        only if the grid is complete. i.e, the rightmost column doesn't
        have any gaps
    '''
    # It might be unnecessary to compare against final_date for now.
    # But maybe not in the future
    if event >= start_date and event < final_date:
        latest_events.append(event)
##    else:
##        break

final_date_pretty = final_date.strftime('%A, %b %d, %Y')
start_date_pretty = start_date.strftime('%A, %b %d, %Y')
if not latest_events:
    print(f"There are no events between '{final_date_pretty}' and '{start_date_pretty}'")
    exit()

cells = range((final_date - start_date).days)
print('latest event:', max(latest_events), 'earliest event:', min(latest_events))
print(f'final: {final_date}, start: {start_date}')

def dateRange(start, end):
    current = start
    while current < end:
        yield current
        current += STEP

days = range((final_date - start_date).days)
grid = lambda cols, rows: divmod(cols, rows) 
coords_by_col = []
for day in days:
    coords_by_col.append(grid(day, DAYS_PER_WEEK))

first_run = 0
month_coords = []
for offset in days:
    current = start_date + dt.timedelta(days=offset)
    last_day_of_this_month = monthrange(current.year, current.month)[1]
    if first_run == 0:
        first_run += 1
        first_month = current.month
    if current.day == last_day_of_this_month:
        coord = grid((current - start_date).days, DAYS_PER_WEEK)
        month_coords.append(coord)

max_index = coords_by_col[-1][0]
columns = [[coord for coord in coords_by_col if coord[0] == i] for i in range(max_index + 1)]

event_coords = []
for event in latest_events:
    coord = grid((event - start_date).days, DAYS_PER_WEEK)
    event_coords.append(coord)

# EOM means end of month
eom_coords = []
for date in dateRange(start_date, final_date):
    if date.day == monthrange(date.year, date.month):
        date += STEP * 6
        print('a')
        eom_coords.append(grid(date - start_date).days, DAYS_PER_WEEK)

coords_by_row = sorted(coords_by_col, key=itemgetter(1, 0))
##for i, (a, b) in enumerate(zip(coords_by_col, coords_by_row)):
##    print(f'{i:>3}.  {str(a):>7} - {str(b):>7}', end='')
##    print()

latest_row = 0
first_weekday = 0 
##def printMonth(coords):
##    for col, row in coords:
##        if col[]
##    return

##for col, row in coords:
##    if row == latest_row: 
##        print(col, end='')
##    else:
##        print()
##        break

def checkEvent(coord):
    if coord in event_coords:
        return('x')
    else:
        return('.')

##for coord in coords_by_col:
##    if coord in month_coords:
##        print('a', end=' ')
##    else:
##        print('', end='')
count = 0
print(' ' * 4, end='')
for col in range(max_index + 1):
##    for coord in columns[col]:
    if any(coord in month_coords for coord in columns[col]):
        print(MONTHS[count % len(MONTHS)], end='')
        count += 1
    else:
        print(' ', end='')

print()
for coord in coords_by_row:
    tile = checkEvent(coord)
    if first_weekday == 0:
        print(WEEKDAYS[coord[ROW]], end=' ')
        first_weekday = 1
    if coord[ROW] == latest_row:
        print(tile, end='')
    else:
        latest_row = coord[ROW]
        print()
        print(WEEKDAYS[coord[ROW]], end=' ')
        print(tile, end='')

print()
##for cell in cells:
##    if (cell + 1) % 7:
##        print('.', end='')
##    else:
##        print('.')
