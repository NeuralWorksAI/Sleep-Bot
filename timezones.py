from datetime import datetime, timedelta

def dtstring(time):
    newtime = str(time).split(":")
    return newtime[0][-2:]+":"+newtime[1][-2:]

def utc_to_local(time, tz):
    time = str(time)
    time = datetime.strptime(time, '%Y-%m-%d %H:%M:%S.%f')
    return time - timedelta(minutes=tz)