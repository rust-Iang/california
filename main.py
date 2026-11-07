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
#days_per_year = 366 if isleap(last_event.year) else 365
DAYS_PER_YEAR = 365
COLS = 53

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
# recent date in the list
final_date = events[0] if not args.today else dt.date.today()
start_date = final_date - dt.timedelta(DAYS_PER_YEAR + DAYS_PER_WEEK - 1)

latest_events = []
for event in events:
    '''
        Selects just the latest event dates to operate on.

        In Github, the whole contribution grid is 53*7 (371), that is
        only if the grid is complete. i.e, the rightmost column doesn't
        have any gaps
    '''
    if event >= start_date:
        latest_events.append(event)
    else:
        break

#start_date = dt.datetime.fromisoformat(str(last_event.year) + '-01-01')
#start_date.weekday() # this is the gap at the start


coords = []
for col in range(COLS): 
    coords.append(divmod(col, DAYS_PER_WEEK))

number_of_weeks = coords[-1][0] # last item, then the first element inside the tuple

event_coords = []
for date in dates:
    day_of_year = (date - start_date).days
    coord = divmod(day_of_year + offset, rows)
    event_coords.append(coord)

#def printEvent(n, days_with_events):
#    if n in days_with_events:
#        print('x', end='')
#    else:
#        print('.', end='')

coords = sorted(coords, key=itemgetter(1, 0))

#real_count = 0
for col, row in coords:
    print(col, row)
 
#for coord in coords_sorted:
#    if count < number_of_weeks:
#        printEvent(coord, event_coords)
#        count +=1
#    else:
#        real_count += count
#        if real_count == year_in_days:
#            print()
#            break
#        else:
#            count = 1
#            print() # Newline
#            printEvent(coord, event_coords)

#print(*coords_sorted, sep='\n')
#print(*coords, sep='\n')
#for i, coord in enumerate(coords):
#    print(coord)
