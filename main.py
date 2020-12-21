import time, datetime
import gpxpy
import xml.etree.ElementTree as ET
import os
import sys
import re
import arrow


class GpxStravaFileMaker:
    def __init__(self, filename, date):
        self.timenew = date
        self.filename = filename
        # defs
        ET.register_namespace('', "http://www.topografix.com/GPX/1/1")
        ET.register_namespace("", "http://www.topografix.com/GPX/1/1/gpx.xsd")
        ET.register_namespace("", "http://www.w3.org/2001/XMLSchema-instance")
        ET.register_namespace("", "http://www.topografix.com/GPX/1/1")

        self.tree = ET.parse(filename)
        self.root = self.tree.getroot()

        # get timedelta
        print("previous activity start time: ", self.root[0][0].text)
        self.timedelta = self.timedeltaget(self.root[0][0].text, self.timenew)
        print("time delta: ", self.timedelta)

    def timedeltaget(self, time1, time2):
        timed = arrow.get(time1) - arrow.get(time2)
        return timed

    def getnewdate(self, old_date, timedelta):
        old_date = arrow.get(old_date).datetime
        new_date = old_date - timedelta
        new_date = str(new_date)
        new_date = re.sub(" ", "T", new_date)
        new_date = re.sub("\+00:00", "Z", new_date)
        return new_date

    def changeInitTime(self):
        # change initial time of gpx
        self.root[0][0].text = self.getnewdate(self.root[0][0].text, self.timedelta)
        print("new start time: ", self.root[0][0].text)

    def changeAllTimes(self):
        # change time and date in gps recordings
        for child in self.root[1][2]:
            # change date and time
            new_date_gpx = self.getnewdate(child[1].text, self.timedelta)
            # write date and time to gpx
            child[1].text = new_date_gpx
            print(new_date_gpx)

    def saveToFile(self, filename):
        # save the file
        self.tree.write("newactivity.gpx")


if __name__ == '__main__':
    timenew = input("time[YYYY-MM-DDThh:mm:ssZ]>> ")
    fileMaker = GpxStravaFileMaker(input("filename>> "), timenew)
    fileMaker.changeInitTime()
    fileMaker.changeAllTimes()
    fileMaker.saveToFile(input("filename>> "))


