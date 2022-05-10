# functions regarding the timer and matching the time submitted to actual time
import time


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