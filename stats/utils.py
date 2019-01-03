from datetime import date
from datetime import timedelta
import os

def dateLastStartOfWeek():
    today = date.today()
    day_of_week = os.environ.get('START_OF_WEEK','Monday').lower()

    day_offset = 0
    if day_of_week == "tuesday":
        day_offset = 1
    elif day_of_week == "wednesday":
        day_offset = 2
    elif day_of_week == "thursday":
        day_offset = 3
    elif day_of_week == "friday":
        day_offset = 4
    elif day_of_week == "saturday":
        day_offset = 5
    elif day_of_week == "sunday":
        day_offset = 6
    offset = (today.weekday() - day_offset) % 7
    last_week_start = today - timedelta(days=offset)
    return last_week_start
