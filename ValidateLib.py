import datetime

def ValidateDate(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return date
    except ValueError:
        return None
#Validates date string

def ValidateTime(time):
    try:
        datetime.datetime.strptime(time, '%H:%M')
        return time
    except ValueError:
        return None
#Validates time string
