import time, datetime
import gpxpy
import xml.etree.ElementTree as ET
import os
import sys
import re
import arrow


def timedeltaget(time1, time2):
    timed = arrow.get(time1) - arrow.get(time2)
    return timed


def getnewdate(old_date, timedelta):
    old_date = arrow.get(old_date).datetime
    new_date = old_date - timedelta
    new_date = str(new_date)
    new_date = re.sub(" ", "T", new_date)
    new_date = re.sub("\+00:00", "Z", new_date)
    return new_date


# defs
ET.register_namespace('', "http://www.topografix.com/GPX/1/1")
ET.register_namespace("", "http://www.topografix.com/GPX/1/1/gpx.xsd")
ET.register_namespace("", "http://www.w3.org/2001/XMLSchema-instance")
ET.register_namespace("", "http://www.topografix.com/GPX/1/1")

# inputs
tree = ET.parse(input("path>> "))
root = tree.getroot()
timenew = input("time[YYYY-MM-DDThh:mm:ssZ]>> ")

# get timedelta
print("previous activity start time: ", root[0][0].text)
_timedelta = timedeltaget(root[0][0].text, timenew)
print("time delta: ", _timedelta)

# change initial time of gpx
root[0][0].text = getnewdate(root[0][0].text, _timedelta)
print("new start time: ", root[0][0].text)


# change time and date in gps recordings
for child in root[1][2]:
    # change date and time
    new_date_gpx = getnewdate(child[1].text, _timedelta)
    # write date and time to gpx
    child[1].text = new_date_gpx
    print(new_date_gpx)

# save the file
tree.write("newactivity.gpx")
