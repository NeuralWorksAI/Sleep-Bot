import datetime
from math import floor

timezones = {
"GMT":0,
"UTC":0,
"ECT":1,
"EET":2,
"ART":2,
"EAT":2,
"MET":3.5,
"NET":4,
"PLT":5,
"IST":5.5,
"BST":6,
"VST":7,
"CTT":8,
"JST":9,
"ACT":9.5,
"AET":10,
"SST":11,
"NST":12,
"MIT":13,
"HST":14,
"AST":15,
"PST":16,
"PNT":17,
"MST":17,
"CST":18,
"EST":19,
"IET":19,
"PRT":20,
"CNT":20.5,
"AGT":21,
"BET":21,
"CAT":2
}

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
    print(hours, minutes)
    return datetime.time(hours, minutes)


def get_time(time, tz):
    time = str(time)
    time = time.split(":")
    hours = int(time[0])-floor(tz)
    minutes = int(time[1])
    if isinstance(tz, float):
        minutes -= 30
    return intdatetime(hours, minutes)

def utc_to_local(time, tz):
    #Okay this is a really terrible way of doing this but it is 3am
    time = str(time)
    time = time.split(":")
    hours = floor(tz)+int(time[0])
    minutes = int(time[1])
    if isinstance(tz, float):
        minutes += 30
    return intdatetime(hours, minutes)

print(utc_to_local("18:00", 5.5))