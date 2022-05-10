# functions regarding the timer and matching the time submitted to actual time
import time

# time.sleep(t) can be used to say do nothing for t number of seconds
# for example we can do it every 59 seconds
# this way we don't have to constantly check for the time 

# for more info:
# https://docs.python.org/3/library/time.html

def getTime():
    return time.asctime()[11:19]

def getPresetTime():
    # function to receive time given from the web app
    return

def checkTimeMatches():
    if getTime() == getPresetTime():
        return True
    else:
        return False