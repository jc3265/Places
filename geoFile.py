#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv         #Csv library
import requests    #Url Requests library
import re          #Return Library
from googleplaces import GooglePlaces, types, lang # Import Google Places library
from geopy.distance import great_circle #Distance formula
import datetime
import calendar
import math
from pygeocoder import Geocoder
import string
import os

Key = '' #API Key
myGeocoder = Geocoder(api_key=Key)
google_places = GooglePlaces(Key) #Initialize GooglePlaces object
myTextFile = '/home/zrtho/Documents/pythonTest/output1.txt' #output file for comparisons
inputFile = '/home/zrtho/Documents/csvFilesWithTimeStamp/smallPyTest.csv'
outputFile = '/home/zrtho/Documents/PyOutput/output2.csv'
placesFile = '/home/zrtho/Documents/PyOutput/listOfPlaces.csv'
places = []


#Not working, even though the list contains the place it is not found when looking for it
'''
def loadPlaces(fileName):
    places = []
    if os.stat(fileName).st_size <10 :
        print "empty"
    else:
        with open(fileName, 'r') as inputPlaces:
            myCsvFile = csv.reader(inputPlaces, delimiter=',')
            for row in myCsvFile:
                placeName = str(row[1])
                if placeName in places:
                    print 'pass'
                else:
                    print 'append'
                    places.append(placeName)
    return places
'''
####################################################################################
#   Function that looks for the nearby places of a given latitude and longitude    #
####################################################################################
def build_URL(lat,longit):
    base_url = 'https://maps.googleapis.com/maps/api/place/radarsearch/json?location='# Can change json to xml to change output type
    latitude = str(lat) #Cast String to the Float
    longitude = str(longit) #Cast String to the Float
    radius = '15'   #Radius of search in meters
    radiusString = '&radius='+radius
    typeS = 'all' #types, can be specific such as church, park, gas station, etc...
    typeString = '&type=' + typeS
    key_string = '&key='+Key
    url = base_url+latitude+','+longitude+radiusString+typeString+key_string
    return url

########################################################
#   Function that Writes the url result in json format #
########################################################
def writeToFile(urlResult):
    text_file = open(myTextFile, "w")#Text file where the output will be stored
    text_file.write(str(requests.get(urlResult).json()))
    text_file.close() #close file so that every line is a new file

######################################################################################
#   Function that checks the json file, scans the line for any place_id and if Found #
#           it returns the place_id                                                  #
######################################################################################
def checkTheFile():
    fileToRead = open(myTextFile,"r")#Read the same file and scan for a string
    for line in fileToRead:
        if 'place_id' in line:
            size = len(line.split('place_id'))
            if size == 2:
                place_id = line.split('place_id')[1].replace("',","u'").split("u'")[1]
                return place_id, 1
            elif size == 3 :
                place1 = line.split('place_id')[1].replace("',","u'").split("u'")[1]
                place2 = line.split('place_id')[2].replace("',","u'").split("u'")[1]
                place_id = str(place1)+","+str(place2)
                return place_id, 2
            elif size >= 4:
                place1 = line.split('place_id')[1].replace("',","u'").split("u'")[1]
                place2 = line.split('place_id')[2].replace("',","u'").split("u'")[1]
                place3 = line.split('place_id')[3].replace("',","u'").split("u'")[1]
                place_id = str(place1)+","+str(place2)+","+str(place3)
                return place_id, 3
        else:
            return "Road",0
    fileToRead.close()

#############################################################################
#   Function that uses the place_id and sends a query to the google API and #
#      if the place exists it reurns the place type                         #
#############################################################################
def getPlaceInformation(place_id, latitude, longitude, numberOfPlaces, outpuPlacesFile):
    if place_id == 'Road':
        results = myGeocoder.reverse_geocode(float(latitude), float(longitude))
        #results = geocoder.google([latitude,longitude], method='reverse') # Returns a geocoder object
        placeAddress = str(results).split(',')[0]
        try:
            placeAddress = str(place.name.replace(",", ""))
        except:
            printable = set(string.printable)
            placeAddress = (filter(lambda x: x in printable, placeAddress))
        placeOutput(placeAddress, "Road", latitude, longitude, outpuPlacesFile)#Add Road to the list
        return (placeAddress,"Road",0)
    else:
        if numberOfPlaces == 1:
            place = google_places.get_place(place_id = place_id)
            try:
                placeName = str(place.name.replace(",", "").replace('|',""))
            except:
                printable = set(string.printable)
                placeName = (filter(lambda x: x in printable, place.name))
            a=str(place.geo_location)
            placeLat= a.split("Decimal('")[1].split('\')')[0]
            placeLong=a.split("Decimal('")[2].split('\')')[0]
            placeOutput(placeName, place.types[0], placeLat, placeLong, outpuPlacesFile)#Add place 1 to the list
            return (placeName, place.types[0], 1)
        elif numberOfPlaces == 2:
            #Operations for place 1:
            place1 = place_id.split(',')[0]
            place1 = google_places.get_place(place_id = place1)
            try:
                placeName1 = str(place1.name.replace(",", "").replace('|',""))
            except:
                printable = set(string.printable)
                placeName1 = (filter(lambda x: x in printable, place1.name))
            a=str(place1.geo_location)
            placeLat1= a.split("Decimal('")[1].split('\')')[0]
            placeLong1=a.split("Decimal('")[2].split('\')')[0]
            placeOutput(placeName1, place1.types[0], placeLat1, placeLong1, outpuPlacesFile)
            #Operations for place 2:
            place2 = place_id.split(',')[1]
            place2 = google_places.get_place(place_id = place2)
            try:
                placeName2 = str(place2.name.replace(",", "").replace('|',""))
            except:
                printable = set(string.printable)
                placeName2 = (filter(lambda x: x in printable, place2.name))
            a=str(place2.geo_location)
            placeLat2= a.split("Decimal('")[1].split('\')')[0]
            placeLong2=a.split("Decimal('")[2].split('\')')[0]
            placeOutput(placeName2, place2.types[0], placeLat2, placeLong2, outpuPlacesFile)#Add place 2 to the list
            placeName = str(placeName1)+'|'+str(placeName2) #Return the name of the two places
            placeTypes = str(place1.types[0])+'|'+str(place2.types[0])
            return (placeName, placeTypes,2)
        else:
            #Operations for place 1:
            place1 = place_id.split(',')[0]
            place1 = google_places.get_place(place_id = place1)
            try:
                placeName1 = str(place1.name.replace(",", "").replace('|',""))
            except:
                printable = set(string.printable)
                placeName1 = (filter(lambda x: x in printable, place1.name))
            #except:
            #    placeName1 = place1.name[:-1]
            a=str(place1.geo_location)
            placeLat1= a.split("Decimal('")[1].split('\')')[0]
            placeLong1=a.split("Decimal('")[2].split('\')')[0]
            placeOutput(placeName1, place1.types[0], placeLat1, placeLong1, outpuPlacesFile)
            #Operations for place 2:
            place2 = place_id.split(',')[1]
            place2 = google_places.get_place(place_id = place2)
            try:
                placeName2 = str(place2.name.replace(",", "").replace('|',""))
            except:
                printable = set(string.printable)
                placeName2 = (filter(lambda x: x in printable, place2.name))
            a=str(place2.geo_location)
            placeLat2= a.split("Decimal('")[1].split('\')')[0]
            placeLong2=a.split("Decimal('")[2].split('\')')[0]
            placeOutput(placeName2, place2.types[0], placeLat2, placeLong2, outpuPlacesFile)#Add place 2 to the list
            #Operations for place 3:
            place3 = place_id.split(',')[2]
            place3 = google_places.get_place(place_id = place3)
            try:
                placeName3 = str(place3.name.replace(",", "").replace('|',""))
            except:
                printable = set(string.printable)
                placeName3 = (filter(lambda x: x in printable, place3.name))
            a=str(place3.geo_location)
            placeLat3= a.split("Decimal('")[1].split('\')')[0]
            placeLong3=a.split("Decimal('")[2].split('\')')[0]
            placeOutput(placeName3, place3.types[0], placeLat3, placeLong3, outpuPlacesFile)#Add place 3 to the list
            placeName = str(placeName1)+'|'+str(placeName2)+'|'+str(placeName3) #Return the name of the three places
            placeTypes = str(place1.types[0])+'|'+str(place2.types[0]) +'|'+str(place3.types[0])
            return (placeName, placeTypes,3)

#################################################################################
#   Function that creates a gid, uses placeName, placeType, latitude, longitude #
#     to construct a comma delimited csv file that has the places information   #
#################################################################################
def placeOutput(placeName, placeType, latitude, longitude , outpuPlacesFile):
    myWriter = csv.writer(outpuPlacesFile, quoting=csv.QUOTE_NONE, escapechar=' ')
    if placeName in places:
        pass
    else:
        places.append(placeName)
        myWriter.writerow([places.index(placeName)+1, str(placeName), str(placeType), latitude, longitude])

##############################################################################
#   Function that uses the gid, placeName, placeType, latitude, longitude to #
#               construct a comma delimited csv file                         #
##############################################################################
def outputToCsv(fileName, placeName, placeType, latitude, longitude, numberOfPlaces, speed,occupancy,direction, mph,\
    timediff, distance, day, time, taxiID, row):
    myWriter = csv.writer(fileName, quoting=csv.QUOTE_NONE, escapechar=' ')
    #geom = latitude+','+longitude #Works even for those without a '-' but leaveas a ' ' before the comma
    if numberOfPlaces == 0:
        #points = "POINT("+str(latitude)+str(longitude)+")" #Works nicely if separated by a '-'
        myWriter.writerow([places.index(placeName)+1, str(placeName), str(placeType), latitude, longitude, speed,occupancy, direction, mph,\
        timediff, distance, day, time, taxiID, row])
    elif numberOfPlaces == 1:
        #points = "POINT("+str(latitude)+str(longitude)+")"
        myWriter.writerow([places.index(placeName)+1, str(placeName), str(placeType), latitude, longitude, speed,occupancy, direction, mph,\
        timediff, distance, day, time, taxiID, row])
    elif numberOfPlaces == 2:
        #points = "POINT("+str(latitude)+str(longitude)+")"
        gid = str(places.index(placeName.split("|")[0])+1) +"|"+ str(places.index(placeName.split("|")[1])+1)
        myWriter.writerow([gid, str(placeName), str(placeType), latitude, longitude, speed,occupancy, direction, mph, timediff, distance\
        , day, time, taxiID, row])
    else:
        #points = "POINT("+str(latitude)+str(longitude)+")"
        gid = str(places.index(placeName.split("|")[0])+1) +"|"+ str(places.index(placeName.split("|")[1])+1)\
            + "|"+ str(places.index(placeName.split("|")[2])+1)
        myWriter.writerow([gid, str(placeName), str(placeType), latitude, longitude, speed,occupancy, direction, mph, timediff, distance\
        , day, time, taxiID, row])

###############################################################################
#   Function that takes two time inputs and finds the difference between them #
###############################################################################
def timeDifference(time1, time2):
    if time1 == 0: #check for the first line of the fle
        return 0
    else:
        time1 = datetime.datetime.strptime(str(time1), '%m-%d-%Y %H:%M:%S') # Read and convert the time
        time2 = datetime.datetime.strptime(str(time2), '%m-%d-%Y %H:%M:%S') # Read and convert the time
        timeDiff= time2 - time1
        return timeDiff.total_seconds()

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

##################################################################
#   Function that takes time and distane and returns the speed   #
##################################################################
def speed(time, distance):
    if time ==0:
        return 0
    elif distance == 0:
        return 0
    else:
        return distance / time

###################################################################
#   Function that takes the latitdes and longtudes and Calculates #
#              its direction on the map in degrees                #
#       Credit to: https://gist.github.com/jeromer/2005586        #
###################################################################
def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

#################################################################
#   Function that takes the calculated degrees and returns its  #
#              corres ponding direction on the map              #
#################################################################
def getDirection(compass):
    if compass >=315 or compass <= 45:
        return 'N'
    elif compass >=45 and compass <= 90:
        return 'NE'
    elif compass >=90 and compass <= 135:
        return 'SE'
    elif compass >=135 and compass <= 225:
        return 'S'
    elif compass >=225 and compass <= 270:
        return 'SW'
    else:
        return 'NW'

##################################################################
#   Function that returns the day of the week given certain time #
##################################################################
def getDay(time):
    time = datetime.datetime.strptime(str(time), '%m-%d-%Y %H:%M:%S') # Read and convert the time
    return str(calendar.day_name[time.weekday()])

############
#   Main   #
############
def driver(taxiID):
    with open(inputFile, 'r') as csvfile:
        taxiID = taxiID
        a = datetime.datetime.now()
    # Format of the CSV: tid|latitude|longitude|occupancy|time|gid|taxi ID
        oneFile = open (outputFile, 'ab+')
        #places = loadPlaces(placesFile) #read and load the places ##Not working ##
        outpuPlacesFile = open (placesFile, 'ab+') #Write to places, 'a' opens the file for appending
        myCsvFile = csv.reader(csvfile, delimiter=',')
        latitude = 0.0
        longitude = 0.0
        time = 0
        myWriter = csv.writer(oneFile, quoting=csv.QUOTE_NONE, escapechar=' ')#Write header to the csv
        #myWriter.writerow(['pId', 'Place Name', 'Place Type', 'latitude', 'longitude', 'Speed (m/s)', 'Occupancy', 'Direction', 'MPH',\
        # 'time Difference', 'Distance', 'Day', 'time Stamp', 'Taxi ID', "Line"])
        for row in myCsvFile:
            tid = int(row[0])
            if taxiID == int(row[6]):
                taxiID = int(row[6])
            else:
                #myWriter.writerow(['New Taxi'])
                taxiID = int(row[6])
                latitude = 0.0
                longitude = 0.0
                time = 0
            distance=distanceTraveled(latitude,longitude,row[1],row[2])
            compass = calculate_initial_compass_bearing((float(latitude),float(longitude)),(float(row[1]),float(row[2])))
            direction = getDirection(compass)
            latitude = row[1]
            longitude = row[2]
            occupancy = int(row[3])
            timediff=timeDifference(time, row[4])
            time = row[4]
            day = getDay(time)
            gid = row[5]
            urlResult= build_URL(latitude,longitude)
            writeToFile(urlResult)
            place_id,numberOfPlaces = checkTheFile()

            placeName,placeType,numberOfPlaces = getPlaceInformation(place_id, latitude, longitude, numberOfPlaces, outpuPlacesFile)
            outputToCsv(oneFile, placeName, placeType, latitude, longitude, numberOfPlaces, speed(timediff, distance)\
            ,occupancy, direction,(speed(timediff, distance) * 2.23694), timediff, distance, day, time, taxiID, int(row[5]))
        oneFile.close()
        outpuPlacesFile.close()
        b = datetime.datetime.now()
        print 'It took:'
        print (b-a).total_seconds()


driver(1)
