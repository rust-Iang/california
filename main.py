#!/bin/env python
import argparse
import subprocess # For running git (we need to dipose this later, to make the program extensible)
import datetime as dt # For all date operations
from calendar import isleap # To decide whether a given year has 366 or 365 days
from operator import itemgetter # To sort the coordinates

parser = argparse.ArgumentParser (
    prog = 'california',
    description = 'Github style grid calendar, now available in your CLI!',
    epilog = 'Submit your own plugins to: https://github.com/rust-Iang/california/'
)
parser.add_argument('-t', '--today', action='store_true')
args = parser.parse_args()

DAYS_PER_WEEK = 7
DAYS_PER_YEAR = 365
WEEKS = 53
SUNDAY = 6
COL = 0
ROW = 1

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
final_date = events[0] if not args.today else dt.datetime.now().replace(microsecond=0)

# The following is the block used to set the start_date variable:
try:
    # Can we make it self aware of the variable we are replacing?
    # Like sys.argv[0]?
    start_date = final_date.replace(year=final_date.year - 1)
    ##start_date = final_date - dt.timedelta(DAYS_PER_YEAR + (week - weekday ))
except ValueError:
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
    if event >= start_date and event <= final_date:
        latest_events.append(event)
    else:
        break

# We need to check if latest_events list is empty
print(max(latest_events), min(latest_events))
print(f'final: {final_date}, start: {start_date}')

cells = range((final_date - start_date).days)
print(cells)
grid = lambda cols, rows: divmod(cols, rows) 
coords = []
for cell in cells:
    coords.append(grid(cell, DAYS_PER_WEEK))

##number_of_weeks = coords[-1][0] # last item, then the first element inside the tuple

##event_coords = []
##for date in dates:
##    day_of_year = (date - start_date).days
##    coord = divmod(day_of_year + offset, rows)
##    event_coords.append(coord)
##
coords = sorted(coords, key=itemgetter(1, 0))



latest_row = 0
for coord in coords:
    if coord[ROW] == latest_row:
        print('.', end='')
    else:
        latest_row = coord[ROW]
        print()
        print('.', end='')
print()
##for cell in cells:
##    if (cell + 1) % 7:
##        print('.', end='')
##    else:
##        print('.')
