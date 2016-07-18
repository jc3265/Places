#!/usr/bin/env python
# -*- coding: utf-8 -*-
import csv         #Csv library
import requests    #Url Requests library
import re          #Return Library
from googleplaces import GooglePlaces, types, lang # Import Google Places library
from geopy.distance import great_circle
import geocoder
import datetime
import math
from pygeocoder import Geocoder
import string

Key = '' #API Key
google_places = GooglePlaces(Key) #Initialize GooglePlaces object
myTextFile = '/home/zrtho/Documents/pythonTest/output1.txt' #output file for comparisons
inputFile = '/home/zrtho/Documents/csvFilesWithTimeStamp/OneLine.csv'
outputFile = '/home/zrtho/Documents/PyOutput/output2.csv'
placesFile = '/home/zrtho/Documents/PyOutput/listOfPlaces.csv'
places = []

#geolocator = Nominatim() #osm Returns an object

####################################################################################
#   Function that looks for the nearby places of a given latitude and longitude    #
####################################################################################
def build_URL(lat,longit):
    base_url = 'https://maps.googleapis.com/maps/api/place/radarsearch/json?location='     # Can change json to xml to change output type
    lat = str(lat) #Cast String to the Float
    longit = str(longit) #Cast String to the Float
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
def writeToFile(url):
    text_file = open(myTextFile, "w")#Text file where the output will be stored
    #text_file.write(str(requests.get(urlResult).text) #Prints nicely in text format
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
def getPlaceInformation(place_id, latitude, longitude, numberOfPlaces):
    if place_id == 'Road':
        results = geocoder.google([latitude,longitude], method='reverse') # Returns a geocoder object
        #print  "pygeocode" + str(Geocoder.reverse_geocode(37.74482, -122.42038))
        #print "Geocoder: " + str(results)
        #print results.address
        placeAddress = results.address.split(',')[0]
        placeOutput(placeAddress, "Road", latitude, longitude)#Add Road to the list
        return (placeAddress,"Road",0)
    else:
        if numberOfPlaces == 1:
            place = google_places.get_place(place_id = place_id)
            placeName = str(place.name.replace(",", ""))
            a=str(place.geo_location)
            placeLat= a.split("Decimal('")[1].split('\')')[0]
            placeLong=a.split("Decimal('")[2].split('\')')[0]
            placeOutput(placeName, place.types[0], placeLat, placeLong)#Add place 1 to the list
            return (placeName, place.types[0], 1)
        elif numberOfPlaces == 2:
            #Operations for place 1:
            place1 = place_id.split(',')[0]
            place1 = google_places.get_place(place_id = place1)
            placeName1 = str(place1.name.replace(",", ""))
            a=str(place1.geo_location)
            placeLat1= a.split("Decimal('")[1].split('\')')[0]
            placeLong1=a.split("Decimal('")[2].split('\')')[0]
            placeOutput(placeName1, place1.types[0], placeLat1, placeLong1)
            #Operations for place 2:
            place2 = place_id.split(',')[1]
            place2 = google_places.get_place(place_id = place2)
            #print "Name"
            #print place2.name
            #print "Place2" + str(place_id)
            try:
                placeName2 = str(place2.name.replace("\xc3\xb1", "n"))
            except:
                printable = set(string.printable)
                placeName2 = (filter(lambda x: x in printable, place2.name))
            a=str(place2.geo_location)
            placeLat2= a.split("Decimal('")[1].split('\')')[0]
            placeLong2=a.split("Decimal('")[2].split('\')')[0]
            placeOutput(placeName2, place2.types[0], placeLat2, placeLong2)#Add place 2 to the list
            placeName = str(placeName1)+'|'+str(placeName2) #Return the name of the two places
            placeTypes = str(place1.types[0])+'|'+str(place2.types[0])
            return (placeName, placeTypes,2)
        else:
        #elif numberOfPlaces == 3:
            #Operations for place 1:
            place1 = place_id.split(',')[0]
            place1 = google_places.get_place(place_id = place1)
            try:
                placeName1 = str(place1.name.replace(",", ""))
            except:
                placeName1 = place1.name[:-1]
            a=str(place1.geo_location)
            placeLat1= a.split("Decimal('")[1].split('\')')[0]
            placeLong1=a.split("Decimal('")[2].split('\')')[0]
            placeOutput(placeName1, place1.types[0], placeLat1, placeLong1)

            #Operations for place 2:
            place2 = place_id.split(',')[1]
            place2 = google_places.get_place(place_id = place2)
            placeName2 = str(place2.name.replace(",", ""))
            a=str(place2.geo_location)
            placeLat2= a.split("Decimal('")[1].split('\')')[0]
            placeLong2=a.split("Decimal('")[2].split('\')')[0]
            placeOutput(placeName2, place2.types[0], placeLat2, placeLong2)#Add place 2 to the list

            #Operations for place 3:
            place3 = place_id.split(',')[2]
            place3 = google_places.get_place(place_id = place3)
            placeName3 = str(place3.name.replace(",", ""))
            a=str(place3.geo_location)
            placeLat3= a.split("Decimal('")[1].split('\')')[0]
            placeLong3=a.split("Decimal('")[2].split('\')')[0]
            placeOutput(placeName3, place3.types[0], placeLat3, placeLong3)#Add place 3 to the list
            placeName = str(placeName1)+'|'+str(placeName2)+'|'+str(placeName3) #Return the name of the three places
            placeTypes = str(place1.types[0])+'|'+str(place2.types[0]) +'|'+str(place3.types[0])
            return (placeName, placeTypes,3)

#################################################################################
#   Function that creates a gid, uses placeName, placeType, latitude, longitude #
#     to construct a comma delimited csv file that has the places information   #
#################################################################################
def placeOutput(placeName, placeType, latitude, longitude):
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
def outputToCsv(fileName, placeName, placeType, latitude, longitude, numberOfPlaces, speed,occupancy,direction, mph):
    myWriter = csv.writer(fileName, quoting=csv.QUOTE_NONE, escapechar=' ')
    #geom = latitude+','+longitude #Works even for those without a '-' but leaveas a ' ' before the comma
    if numberOfPlaces == 0:
        points = "POINT("+str(latitude)+str(longitude)+")" #Works nicely if separated by a '-'
        myWriter.writerow([places.index(placeName)+1, str(placeName), str(placeType), points, speed,occupancy, direction, mph])
    elif numberOfPlaces == 1:
        points = "POINT("+str(latitude)+str(longitude)+")"
        myWriter.writerow([places.index(placeName)+1, str(placeName), str(placeType), points, speed,occupancy, direction, mph])
    elif numberOfPlaces == 2:
        points = "POINT("+str(latitude)+str(longitude)+")"
        gid = str(places.index(placeName.split("|")[0])+1) +"|"+ str(places.index(placeName.split("|")[1])+1)
        myWriter.writerow([gid, str(placeName), str(placeType), points, speed,occupancy, direction, mph])
    else:
        points = "POINT("+str(latitude)+str(longitude)+")"
        gid = str(places.index(placeName.split("|")[0])+1) +"|"+ str(places.index(placeName.split("|")[1])+1)\
            + "|"+ str(places.index(placeName.split("|")[2])+1)
        myWriter.writerow([gid, str(placeName), str(placeType), points, speed,occupancy, direction, mph])

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
#
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

############
#   Main   #
############
with open(inputFile, 'rb') as csvfile:
    a = datetime.datetime.now()
# Format of the CSV: tid|latitude|longitude|occupancy|time|gid|taxi ID
    oneFile = open (outputFile, 'wb')
    outpuPlacesFile = open (placesFile, 'wb')
    myCsvFile = csv.reader(csvfile, delimiter=',')
    latitude = 0.0
    longitude = 0.0
    time = 0
    for row in myCsvFile:
        tid = int(row[0])
        distance=distanceTraveled(latitude,longitude,row[1],row[2])
        compass = calculate_initial_compass_bearing((float(latitude),float(longitude)),(float(row[1]),float(row[2])))
        direction = getDirection(compass)
        latitude = row[1]
        longitude = row[2]
        occupancy = int(row[3])
        timediff=timeDifference(time, row[4])
        time = row[4]
        gid = row[5]
        print gid
        taxiID = row[6]
        urlResult= build_URL(latitude,longitude)
        writeToFile(urlResult)
        place_id,numberOfPlaces = checkTheFile()
        placeName,placeType,numberOfPlaces = getPlaceInformation(place_id, latitude, longitude, numberOfPlaces)
        outputToCsv(oneFile, placeName, placeType, latitude, longitude, numberOfPlaces, speed(timediff, distance)\
        ,occupancy, direction,(speed(timediff, distance) * 2.23694))
    oneFile.close()
    outpuPlacesFile.close()
    b = datetime.datetime.now()
    print 'It took:'
    print (b-a).total_seconds()
