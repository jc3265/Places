#!/usr/bin/env python
# coding=utf-8
import math
import csv
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

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
# pid|placeName|placeType|latitude|longitude|spee##########################################################
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
    latitude = float(latitude)
    longitude = float(longitude)

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

    return point1, point2, point3, point4

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
        if float(leftLong) <= longPoint <= float (rightLong):
            if float(lowerLat) <= latPoint <= float (upperLat):
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
def filterTime(pointsInRange, date, seconds):

    timePoints = []
    margin = datetime.timedelta(seconds = seconds)
    date = datetime.datetime.strptime(str(date), '%m-%d-%Y %H:%M:%S') # Read and convert the time, time format is MM-DD-YY HH-MM-SS
    timeLess = datetime.datetime.strptime(str(date - margin), '%Y-%m-%d %H:%M:%S')
    timeMore = datetime.datetime.strptime(str(date + margin), '%Y-%m-%d %H:%M:%S')

    for x in xrange (0,len(pointsInRange)):
        time = datetime.datetime.strptime(str(pointsInRange[x].getTimeStamp()), '%m-%d-%Y %H:%M:%S')
        if timeLess <= time <= timeMore:
            timePoints.append(pointsInRange[x])
        else:
            pass
    return timePoints

####################################################################################################
#   Function that tries to create a distance based cluster, each of the clusters are stored in the #
#               numberOfclusters and each cluster is composed of multiple points                   #
####################################################################################################
def createCluster(data, searchRange):
    numberOfclusters = []
    cluster0 = []
    searchRange = int(searchRange)
    i = 1
    for x  in xrange (0,len(data)):
        if x == 0:
            cluster0.append(data[x])
            numberOfclusters.insert(0,cluster0)
        else:
            for y in range (0, len(numberOfclusters)):
                point1, point2, point3, point4 = calculateRange(searchRange, numberOfclusters[y][0].getLatitude(), \
                numberOfclusters[y][0].getLongitude())
                leftLat = point4.split(',')[0]
                leftLong = point4.split(',')[1]
                rightLat = point3.split(',')[0]
                rightLong = point3.split(',')[1]
                upperLat = point1.split(',')[0]
                upperLong = point1.split(',')[1]
                lowerLat = point2.split(',')[0]
                lowerLong = point2.split(',')[1]
                longPoint = float(data[x].getLongitude())
                latPoint = float(data[x].getLatitude())
                if float(leftLong) <= longPoint <= float (rightLong):
                    if float(lowerLat) <= latPoint <= float (upperLat):
                        numberOfclusters[y].append(data[x])
                        break
                    else:
                        pass
                else:
                    pass
                if y == (len(numberOfclusters)-1):
                    name = "cluster" + str(i)
                    name = []
                    name.append(data[x])
                    numberOfclusters.append(name)
                    i = i + 1
                    break
                else:
                    pass

    print len(numberOfclusters)
    return numberOfclusters

##############################################################
#   Function that plots the points in an x,y coordinate map  #
##############################################################
def plot(points):
    '''
    x = np.arange(100)
    y = x
    t = x
    plt.scatter(x, y, c=t)
    plt.show()
    cs = [colors[i//len(X)] for i in range(len(Ys)*len(X))]
    '''
    for q in range (0,len(points)):
        for i in range (0, len(points[q])):

            x = 'x'+str(q)
            y = 'y'+str(q)
            x = float(points[q][i].getLongitude())
            y = float(points[q][i].getLatitude())
            plt.scatter(x, y)
    #plt.colorbar()
    plt.show()

############
#   Main   #
############
def driver():
    a = datetime.datetime.now()
    loadPlaces(placesFile)
    loadPoints(pointsFile)
    numberOfclusters = createCluster(points, 200)
    #plot(numberOfclusters)
    #nx = 0
    #for x in xrange (0, len(numberOfclusters)):
    #    nx += len(numberOfclusters[x])
    #print nx

    ####################################
    ##THIS BLOCK WORKS
    #tempList = typesList('points')#Or points
    #for x in range (0, len(tempList)):
    #    print tempList[x]


    #for x in xrange (0,len(places)):
    #if "restaurant" in places[x].getType():
    #        print places[x].getName()


    #point1, point2, point3, point4 = calculateRange(3000 ,37.75165, -122.39427)
    #pointsInRange, taxis = getPointsInRangeWithTime(point1, point2, point3, point4,'05-17-2008 06:05:40', 30000)
    #print 'FIRST'
    #print "There are: " + str(len(pointsInRange)) + " points in range from: " + str(len(taxis)) + " different taxis"
    #pir = getPointsInRange(point1, point2, point3, point4)
    #npir = filterTime(pir,'05-17-2008 06:05:40', 3000)
    #print 'SECOND'
    #print "There are: " + str(len(npir))
    #print pointsInRange[3].getTimeStamp()
    b = datetime.datetime.now()
    print 'It took:'
    print (b-a).total_seconds()

####################################
driver()
#print point3 +"| " + point0
