#!/usr/bin/env python
# coding=utf-8
import math
import csv
import datetime

EARTH_RADIUS = float(6378137) # Global average radii, Equatorial radius in meters

pointsFile = '/home/zrtho/Documents/PyOutput/output2.csv'
placesFile = '/home/zrtho/Documents/PyOutput/100places.csv'
points = []
places = []
#latitude = y axis
#longitude = x axis

class filePoints:
    def __init__(self, pid, placeName, placeType, latitude, longitude, speed, occupancy, direction, mph, timeDiff, distance, day, timeStamp, taxiID):
        self.pid = pid
        self.placeName = placeName
        self.placeType = placeType
        self.latitude = latitude
        self.longitude = longitude
        self.speed = speed
        self.occupancy = occupancy
        self.direction = direction
        self.mph = mph
        self.distance = distance
        self.timeDiff= timeDiff
        self.day = day
        self.timeStamp = timeStamp
        self.taxiID = taxiID

    def getPid(self):
        return self.pid

    def getName(self):
        return self.placeName

    def getType(self):
        return self.placeType

    def getLatitude(self):
        return self.latitude

    def getLongitude(self):
        return self.longitude

    def getSpeed(self):
        return self.speed

    def getOccupancy(self):
        return self.occupancy

    def getDirection(self):
        return self.direction

    def getMph(self):
        return self.mph

    def getDistance(self):
        return self.distance

    def getDay(self):
        return self.day

    def getTimeStamp(self):
        return self.timeStamp

    def getTaxiID(self):
        return self.taxiID

class filePlaces:
    def __init__(self, pid, placeName, placeType, latitude, longitude):
        self.pid = pid
        self.placeName = placeName
        self.placeType = placeType
        self.latitude = latitude
        self.longitude = longitude

    def getPid(self):
        return self.pid

    def getName(self):
        return self.placeName

    def getType(self):
        return self.placeType

    def getLatitude(self):
        return self.latitude

    def getLongitude(self):
        return self.longitude

##########################################################################################################
#           Function that loads the points from a given file whose format is                             #
# pid|placeName|placeType|latitude|longitude|speed|occupancy|direction|mph|distance|day|timeStamp|taxiID #
##########################################################################################################
def loadPoints(fileName):
    with open(fileName, 'r') as csvfile:
        myCsvFile = csv.reader(csvfile, delimiter=',')
        for row in myCsvFile:
            aPoint = filePoints(row[0],row[1],row[2],row[3],row[4],row[5],row[6],row[7],row[8],row[9],row[10],row[11],row[12], row[13])
            points.append(aPoint)

######################################################################
#   Function that loads the places from a given file whose format is #
#            pid|placeName|placeType|latitude|longitude              #
######################################################################
def loadPlaces(fileName):
    with open(fileName, 'r') as csvfile:
        myCsvFile = csv.reader(csvfile, delimiter=',')
        for row in myCsvFile:
            aPoint = filePlaces(row[0], row[1], row[2], row[3], row[4])
            places.append(aPoint)
            #print "APPENDING"

##################################################################
#   Function that returns a list with the available places types #
##################################################################
def typesList(listToSearch):
    tempList = []
    if listToSearch.lower() == 'places'.lower():
        for x in xrange (0,len(places)):
            placeType = places[x].getType()
            if placeType in tempList:
                pass
            else:
                tempList.append(placeType)
        return tempList
    else:
        for x in xrange (0,len(points)):
            placeType = points[x].getType()
            if placeType in tempList:
                pass
            else:
                tempList.append(placeType)
        return tempList

###########################################################
#   Function that returns a list with the available names #
###########################################################
def namesList(listToSearch):
    nameList = []
    if listToSearch.lower() == 'places'.lower():
        for x in xrange (0,len(places)):
            placeName = places[x].getName()
            if placeName in nameList:
                pass
            else:
                nameList.append(placeName)
        return nameList
    else:
        for x in xrange (0,len(points)):
            placeName = points[x].getName()
            if placeName in nameList:
                pass
            else:
                nameList.append(placeName)
        return nameList

#################################################################################
# Function that returns a range of values depending on the source point and the #
# desired radius of interest Using Williams Aviation Formula which states that  #
#               1degree is approximately equal to 111.111 km                    #
#################################################################################
def calculateRange(searchRange, latitude, longitude): # Meters, float, float
    offsetLat = (searchRange/EARTH_RADIUS)
    offsetLong = (searchRange/(EARTH_RADIUS* math.cos((math.pi*latitude)/180)))
    newLat = offsetLat * (180/math.pi)
    newLong = offsetLong * (180/math.pi)
    point0 = str(latitude)+ "," + str(longitude)
    p1 = latitude + newLat
    p2 = latitude - newLat
    p3 = longitude + newLong
    p4 = longitude - newLong
    point1 = str(p1)+","+str(longitude)
    point2 = str(p2)+","+str(longitude)
    point3 = str(latitude) + "," + str(p3)
    point4 = str(latitude) + "," + str(p4)

    return point1, point2, point3, point4, point0

###################################################################
# This method returns the points in range given a set of 4 points #
###################################################################
def getPointsInRange(point1, point2, point3, point4):

    pointsInRange = []

    leftLat = point4.split(',')[0]
    leftLong = point4.split(',')[1]
    rightLat = point3.split(',')[0]
    rightLong = point3.split(',')[1]
    upperLat = point1.split(',')[0]
    upperLong = point1.split(',')[1]
    lowerLat = point2.split(',')[0]
    lowerLong = point2.split(',')[1]

    for x in xrange (0,len(points)):
        longPoint = float(points[x].getLongitude())
        latPoint = float(points[x].getLatitude())
        if float(leftLong) < longPoint < float (rightLong):
            if float(lowerLat) < latPoint < float (upperLat):
                pointsInRange.append(points[x])
            else:
                pass
        else:
            pass
    return pointsInRange

#################################################################################################
# This method returns the points in range given a set of 4 points and a range from a given date #
#################################################################################################
def getPointsInRangeWithTime(point1, point2, point3, point4, date, timeRange):

    pointsInRange = []
    taxis = []
    timerange = int(timeRange)

    margin = datetime.timedelta(seconds = timeRange)
    date = datetime.datetime.strptime(str(date), '%m-%d-%Y %H:%M:%S') # Read and convert the time, time format is MM-DD-YY HH-MM-SS
    timeLess = datetime.datetime.strptime(str(date - margin), '%Y-%m-%d %H:%M:%S')
    timeMore = datetime.datetime.strptime(str(date + margin), '%Y-%m-%d %H:%M:%S')

    leftLat = point4.split(',')[0]
    leftLong = point4.split(',')[1]
    rightLat = point3.split(',')[0]
    rightLong = point3.split(',')[1]
    upperLat = point1.split(',')[0]
    upperLong = point1.split(',')[1]
    lowerLat = point2.split(',')[0]
    lowerLong = point2.split(',')[1]

    for x in xrange (0,len(points)):
        longPoint = float(points[x].getLongitude())
        latPoint = float(points[x].getLatitude())
        time = datetime.datetime.strptime(str(points[x].getTimeStamp()), '%m-%d-%Y %H:%M:%S') # Read and convert the time, time format is MM-DD-YY HH-MM-SS
        if float(leftLong) < longPoint < float (rightLong):
            if float(lowerLat) < latPoint < float (upperLat):
                if timeLess <= time <= timeMore:
                    pointsInRange.append(points[x])
                    if points[x].getTaxiID() in taxis:
                        pass
                    else:
                        taxis.append(points[x].getTaxiID())
                else:
                    pass
            else:
                pass
        else:
            pass
    return pointsInRange, taxis

################################################################################################
#   Function that takes the result of the first filter and re-scans with a given second Filter #
################################################################################################
def secondFilter(pointsInRange, filterType, date, seconds):
    margin = datetime.timedelta(seconds = seconds)
    time = datetime.datetime.strptime(str(date), '%m-%d-%Y %H:%M:%S') # Read and convert the time, time format is MM-DD-YY HH-MM-SS

    print 'asdsadsa'

def driver():
    loadPlaces(placesFile)
    loadPoints(pointsFile)
    tempList = typesList('points')#Or points
    #for x in range (0, len(tempList)):
    #    print tempList[x]


    #for x in xrange (0,len(places)):
    #if "restaurant" in places[x].getType():
    #        print places[x].getName()

    point1, point2, point3, point4, point0 = calculateRange(30 ,37.75165, -122.39427)
    pointsInRange, taxis = getPointsInRangeWithTime(point1, point2, point3, point4,'05-17-2008 06:05:40', 3000)
    print "There are: " + str(len(pointsInRange)) + " points in range from: " + str(len(taxis)) + " different taxis"
    #print pointsInRange[3].getTimeStamp()

#loadPlaces()
#loadPoints()
driver()
#print point3 +"| " + point0
