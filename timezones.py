import datetime
from math import floor

#Okay this is a really terrible way of doing this but it is 3am
def intdatetime(hours, minutes):
    if minutes > 59:
        minutes -= 60
        hours += 1
    elif minutes < 0:
        minutes += 60
        hours -= 1
    if hours > 23:
        hours -= 24
    elif hours < 0:
        hours += 24
    return datetime.time(hours, minutes)

def get_time(time, tz):
    time = str(time)
    time = time.split(":")
    hours = int(time[0])-floor(tz)
    minutes = int(time[1])
    if floor(tz) != tz:
        minutes -= 30
    return intdatetime(hours, minutes)

def utc_to_local(time, tz):
    time = str(time)
    time = time.split(":")
    hours = floor(tz)+int(time[0])
    minutes = int(time[1])
    if floor(tz) != tz:
        minutes += 30
    return intdatetime(hours, minutes)