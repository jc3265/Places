#!/usr/bin/env python
# coding=utf-8
import math
import sys
import csv
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm  # Color Map
from geoFile import timeDifference
from geopy.distance import great_circle #Distance formula
from random import randint


EARTH_RADIUS = float(6378137) # Global average radii, Equatorial radius in meters

pointsFile = '/home/zrtho/Documents/PyOutput/output1.csv'
#pointsFile = '/home/zrtho/Documents/PyOutput/taxiTwo.csv'
placesFile = '/home/zrtho/Documents/PyOutput/100places.csv'
points = []
places = []

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

    def getTimeDifference(self):
        return self.timeDiff

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

##################################################################################
#       Function that loads the points from a given file whose format is         #
# pid|placeName|placeType|latitude|longitude|Speed (m/s)|Occupancy|Direction|MPH #
#               time Difference|Distance|Day|time Stamp|Taxi ID'                 #
##################################################################################
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
def namesList(listToSearch, name):
    nameList = []
    if name.lower() == 'places'.lower():
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
#               1 degree is approximately equal to 111.111 km                   #
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
        time = datetime.datetime.strptime(str(points[x].getTimeStamp()), '%m-%d-%Y %H:%M:%S')
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

####################################################################################
# This method returns the points in range given a set of 4 points and a given date #
####################################################################################
def getPointsInRangeWithDate(point1, point2, point3, point4, date):
    pointsInRange = []
    taxis = []
    date = datetime.datetime.strptime(str(date), '%m-%d-%Y %H:%M:%S') # Read and convert the time, time format is MM-DD-YY HH-MM-SS
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
        time = datetime.datetime.strptime(str(points[x].getTimeStamp()), '%m-%d-%Y %H:%M:%S')
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
    date = datetime.datetime.strptime(str(date), '%m-%d-%Y %H:%M:%S')
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
    #print len(numberOfclusters)
    return numberOfclusters

####################################################################################################
#   Function that tries to create a distance based cluster, each of the clusters are stored in the #
#               numberOfclusters and each cluster is composed of multiple points                   #
####################################################################################################
def createSameDayCluster(data, searchRange):
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
                date = datetime.datetime.strptime(str(numberOfclusters[y][0].getTimeStamp()), '%m-%d-%Y %H:%M:%S')
                clusterDay = date.date()
                date2 = datetime.datetime.strptime(str(data[x].getTimeStamp()), '%m-%d-%Y %H:%M:%S')
                pointDay = date2.date()
                if clusterDay == pointDay:
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
    return numberOfclusters

def createWindow(data):
    windows = []
    cluster0 = []
    i = 1
    inOrder = sorted(data,key=lambda x: x.getTimeStamp(), reverse=False)
    time = 15
    for x in xrange (0, len(data)):
        if x == 0:
            cluster0.append(inOrder[x])
            windows.insert(0, cluster0)
        else:
            for y in range (0, len(windows)):
                pointDate = datetime.datetime.strptime(str(inOrder[x].getTimeStamp()), '%m-%d-%Y %H:%M:%S').date()
                clusterDate = datetime.datetime.strptime(str(windows[y][0].getTimeStamp()), '%m-%d-%Y %H:%M:%S').date()
                if clusterDate == pointDate:
                    clusterHour = datetime.datetime.strptime(str(windows[y][0].getTimeStamp()), '%m-%d-%Y %H:%M:%S').hour
                    pointHour = datetime.datetime.strptime(str(inOrder[x].getTimeStamp()), '%m-%d-%Y %H:%M:%S').hour
                    if pointHour == clusterHour:
                        pointMinute = int(datetime.datetime.strptime(str(inOrder[x].getTimeStamp()), '%m-%d-%Y %H:%M:%S').minute)
                        clusterMinute = int(datetime.datetime.strptime(str(windows[y][0].getTimeStamp()), '%m-%d-%Y %H:%M:%S').minute)

                        if clusterMinute < 5:
                            rng = 5
                        elif clusterMinute < 10:
                            rng = 10
                        elif clusterMinute < 15:
                            rng = 15
                        elif clusterMinute < 20:
                            rng = 20
                        elif clusterMinute < 25:
                            rng = 25
                        elif clusterMinute < 30:
                            rng = 30
                        elif clusterMinute < 35:
                            rng = 35
                        elif clusterMinute < 40:
                            rng = 40
                        elif clusterMinute < 45:
                            rng = 45
                        elif clusterMinute < 50:
                            rng = 50
                        elif clusterMinute < 55:
                            rng = 55
                        else:
                            rng = 60

                        if pointMinute < rng:
                            windows[y].append(inOrder[x])
                            break
                        else:
                            pass
                    else:
                        pass
                else:
                    pass
                if y == (len(windows)-1):
                    name = "cluster" + str(i)
                    name = []
                    name.append(inOrder[x])
                    windows.append(name)
                    i = i + 1
                    break
                else:
                    pass
    return windows

####################################################################################################
#   Function that tries to create a distance based cluster, each of the clusters are stored in the #
#               numberOfclusters and each cluster is composed of multiple points                   #
####################################################################################################
def createSameDayandTaxi(data, searchRange):
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
                clusterTaxi = int(numberOfclusters[y][0].getTaxiID())
                pointTaxi = int(data[x].getTaxiID())
                date = datetime.datetime.strptime(str(numberOfclusters[y][0].getTimeStamp()), '%m-%d-%Y %H:%M:%S')
                clusterDay = date.date()
                date2 = datetime.datetime.strptime(str(data[x].getTimeStamp()), '%m-%d-%Y %H:%M:%S')
                pointDay = date2.date()
                if clusterTaxi == pointTaxi:
                    if clusterDay == pointDay:
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
    return numberOfclusters

###################################################################################
#   Function that takes a list, and finds the points that meet the criteria given #
#        by the user(Average Speedm Average Time) and also considers range        #
###################################################################################
def findStops(data, averageSpeed, averageTime):
    inOrder = sorted(data,key=lambda x: x.getTimeStamp(), reverse=False)
    listOfLists = createSameDayCluster(data, 10)
    stops = []
    for q in range (0,len(listOfLists)):
        speed=0
        time = 0
        for x in range(0, len(listOfLists[q])):
            speed += float(listOfLists[q][x].getMph())
            speedAverage = speed/len(listOfLists[q])
            time += float(listOfLists[q][x].getTimeDifference())
            timeAverage = time /len(listOfLists[q])
        if speedAverage <= float(averageSpeed) and timeAverage <= float(averageTime):
            stops.append(listOfLists[q][x])
    return stops

######################################################################
#   Function that plots the cluster points in an x,y coordinate map  #
######################################################################
def plotClusters(points):
    colors = []
    for q in range (len(points)):
        colors.append('%06X' % randint(0, 0xFFFFFF))
    for q in range (0,len(points)):
        nameX= 'xpoints'+str(q)
        nameY= 'ypoints'+str(q)
        nameX=[]
        nameY=[]
        for i in range (0, len(points[q])):
            nameX.append(float(points[q][i].getLongitude()))
            nameY.append(float(points[q][i].getLatitude()))
        plt.scatter(nameX, nameY, color = '#'+colors[q])
        #plt.plot(nameX, nameY, marker= 'o', markerfacecolor = 'o')
    #plt.axis([0,5,0,5])
    plt.show()

##############################################################
#   Function that plots the points in an x,y coordinate map  #
##############################################################
def plot(points):
    #xPoints = []
    #yPoints = []
    pts = sorted(points,key=lambda x: x.getTaxiID(), reverse=False)
    w=0
    nameX= 'xpoints'+str(pts[0].getTaxiID())
    nameY= 'ypoints'+str(pts[0].getTaxiID())
    for q in range (0, len(pts)):
        try:
            if int(pts[q].getTaxiID()) == int(pts[q+1].getTaxiID()):
                nameX.append(float(pts[q].getLongitude()))
                nameY.append(float(pts[q].getLatitude()))
            else:
                w+=1
                nameX= "xpoints"+str(pts[q].getTaxiID())
                nameY= "ypoints"+str(pts[q].getTaxiID())
                nameX=[]
                nameY=[]
            #plt.scatter(nameX, nameY, color = '#'+colors[q])
            plt.plot(nameX, nameY, marker= 'o', markerfacecolor = 'r')
        except:
            pass
    #plt.colorbar()
    #plt.axis([-122.432,-122.389,37.745,37.792])
    plt.show()

####################################################################
#   Function that plots the speed points in an x,y coordinate map  #
####################################################################
def plotSpeed(points):
    xPoints = []
    yPoints = []
    w=-1
    for q in range (0, len(points)):
        date = datetime.datetime.strptime(str(points[q].getTimeStamp()), '%m-%d-%Y %H:%M:%S')
        w += 1
        xPoints.append(w)
        mph = float(points[q].getMph())
        yPoints.append(mph)
    plt.plot(xPoints, yPoints, marker= 'o', markerfacecolor = 'r')
    #plt.colorbar()
    #plt.axis([0,120,0,1])
    plt.show()

#############################################################################
#   Function that takes a set of two latitudes and longitudes and finds the #
#                distance using the great_circle formula                    #
#############################################################################
def distanceTraveled(lat1, long1, lat2, long2):
    if float(lat1) == 0:
        return 0
    else:
        loc1 = (float(lat1), float(long1))
        loc2 = (float(lat2), float(long2))
        return(great_circle(loc1, loc2).meters)

def getClusterMembers(clusterList):
    for x in xrange (0,len(clusterList)):
        print "Cluster: " + str(x)
        for q in range (0, len(clusterList[x])):
            print str (clusterList[x][q].getTaxiID()) + " " + str (clusterList[x][q].getTimeStamp())

def createWindowClusters(windows):
    try:
        for x in xrange(0, len(windows)):
            smallDistance = sys.maxint
            print "For Window: " + str(x)
            inOrder = sorted(windows[x],key=lambda point: point.getTaxiID(), reverse=False)
            done = False
            tries = 0
            index = 0
            while ((not done) and (int(tries) <= int(10))) :
                for q in range (0, len (inOrder)):

                    ranNum = randint(0, len(inOrder)-1)
                    distance = distanceTraveled(inOrder[ranNum].getLatitude(), inOrder[ranNum].getLongitude(), inOrder[q].getLatitude(), inOrder[q].getLongitude())
                    if int(inOrder[ranNum].getTaxiID()) == int(inOrder[q].getTaxiID()):
                        ranNum += 1
                    else:
                        if distance < smallDistance:
                            print "Another between Taxi: " + str(inOrder[ranNum].getTaxiID()) + " and Taxi: " + \
                                str(inOrder[index].getTaxiID()) + " their distance is: " + str(smallDistance) + "m, their direction is: "\
                                + str(inOrder[ranNum].getDirection()) + " and: " + str(inOrder[index].getDirection())
                            smallDistance = distance
                            index = q
                        else:
                            taxiID = int (inOrder[q].getTaxiID())
                if smallDistance > 200:
                    ranNum = randint(0, len(inOrder)-1)
                    tries += 1
                    done = False
                else:
                    done = True
                if smallDistance < 400 :
                    print "The most similar points are between Taxi: " + str(inOrder[ranNum].getTaxiID()) + " and Taxi: " + \
                        str(inOrder[index].getTaxiID()) + " their distance is: " + str(smallDistance) + "m, their direction is: "\
                        + str(inOrder[ranNum].getDirection()) + " and: " + str(inOrder[index].getDirection())
                else:
                    print "No relationships found for the given time window"

    except Exception as e:
        print e

def analyzeWindow(windows):
    members = []

    for y in range (0, len(windows[0])):
        if int(windows[0][y].getTaxiID()) in members:
            pass
        else:
            members.append(int(windows[0][y].getTaxiID()))

    print "Window 0 has: " + str(len(members)) + " Different taxis"

    members1=[]
    for y in range (0, len(windows[2])):
        if int(windows[2][y].getTaxiID()) in members:
            pass
        else:
            print "Different" + str(windows[2][y].getTaxiID())
            #members1.append(int(windows[1][y].getTaxiID()))

    print "Window 1 has: " + str(len(members1)) + " Different taxis"

    '''
    for x in xrange (2, 3):
        for q in range (0, len(windows[x])):
            if int(windows[x][q].getTaxiID()) in members:
                #print "Taxi was in the previous window"
                print "Window: " + str(x) + " Taxi: " + str(windows[x][q].getTaxiID())
            else:
                pass
                #members.append(int(windows[x][q].getTaxiID()))
    '''

############
#   Main   #
############
def driver():
    a = datetime.datetime.now() # Program start time

    #print datetime.datetime.strptime(str("05-17-2008 06:22:40"), '%m-%d-%Y %H:%M:%S').minute
    loadPlaces(placesFile)
    loadPoints(pointsFile)

    #print datetime.datetime.strptime(str(points[0].getTimeStamp()), '%m-%d-%Y %H:%M:%S').date()
    #splitWindow(points, 12)
    windows = createWindow(points)
    #analyzeWindow(windows)
    #plotClusters(windows)
    #getClusterMembers(windows)
    createWindowClusters(windows)

    #plot(points)
    #plot(windows[0])
    #plot(windows[1])
    #plot(windows[2])
    #       plot(windows[3])

    '''
    print len(windows)
    total = 0
    for x in xrange(0, len(windows)):
        total += len(windows[x])
        print len(windows[x])

        print total

        print str(len(windows[x])) + "\t" + str(windows[x][0].getTimeStamp())
    members = []
    name0 = []
    i = 0
    r = 0
    for x in xrange (0, len(windows)):
        #name = "members" + str(x)
        for q in range (0, len(windows[0])):
            name0.append(int(windows[0][q].getTaxiID()))
    for q in range (0, len (windows[6])):
        name = "members" + str(x)
        name = []
        if int(windows[6][q].getTaxiID()) in name0:
            i +=1
        else:
            r += 1
    print "R " + str(r)
    print "I " + str (i)

    inOrder = sorted(windows[0],key=lambda pt: pt.getTaxiID(), reverse=False)
    print inOrder[0].getTaxiID()
    print windows[0][0].getTaxiID()
    print "DONE"
    #someTest.append(windows)
    #print someTest[0][0][0]
    #print total
    #    numberOfclusters = createSameDayCluster(points, 10)
    #plot(points)

    getClusterMembers(windows)
    '''
    #plotClusters(windows)
    #plotClusters(points)

    #stops =findStops(points,3,120)
    #print "same day no order"
    #print len(stops)
    #for x in xrange (0, len(stops)):
    #    print str(stops[x].getName()) + " " + str(stops[x].getTimeStamp())

    ####################################
    ##THIS BLOCK WORKS
    #tempList = typesList('points')#Or points
    #for x in range (0, len(tempList)):
    #    print tempList[x]

    # Find for clusters on the same day
    # Find stops

    #point1, point2, point3, point4 = calculateRange(100 ,37.75164, -122.39426)
    #pointsInRange, taxis = getPointsInRangeWithTime(point1, point2, point3, point4,'05-17-2008 06:22:40', 30)

    #print len (pointsInRange)
    #print "There are: " + str(len(pointsInRange)) + " points in range from: " + str(len(taxis)) + " different taxis"

    #pir = getPointsInRange(point1, point2, point3, point4)
    #npir = filterTime(pir,'05-17-2008 06:05:40', 3000)
    #print "There are: " + str(len(pir))
    b = datetime.datetime.now() # Program End time
    #print 'It took:'
    print (b-a).total_seconds()
    #print math.fabs((a-b).total_seconds())

####################################
driver()
