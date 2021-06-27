import datetime

timezones = {
"GMT":0,
"UTC":0,
"ECT":1,
"EET":2,
"ART":2,
"EAT":3,
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
"CAT":23
}

def get_time(time, abb):
    if abb not in timezones:
        return
    time = time.split(":")
    tz = timezones[abb]
    if isinstance(tz, float):
        altered_tz = int(tz - 0.5)
        if int(time[1]) + 30 > 60:
            newtime = datetime.time(int(time[0])+altered_tz+1,int(time[1])-30)
        else:
            newtime = datetime.time(int(time[0])+altered_tz,int(time[1])+30)
    else:
        newtime = datetime.time(int(time[0])+tz,int(time[1]))
    return newtime

def utc_to_local(time, abb):
    time = time.split(":")
    tz = timezones[abb]
    if isinstance(tz, float):
        altered_tz = int(tz - 0.5)
        if int(time[1]) + 30 > 60:
            newtime = datetime.time(int(time[0])-altered_tz-1,int(time[1])+30)
        else:
            newtime = datetime.time(int(time[0])-altered_tz,int(time[1])-30)
    else:
        newtime = datetime.time(int(time[0])-tz,int(time[1]))
    return newtime