#!/usr/bin/env python
# coding=utf-8
import string
from googleplaces import GooglePlaces, types, lang
from pygeocoder import Geocoder
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import geocoder
import csv
import math

Key = ''
google_places = GooglePlaces(Key)

#results = geocoder.google([37.74482, -122.42038], method='reverse')
#results = Geocoder.reverse_geocode(37.74482, -122.42038)
#print results
'''
l =google_places.get_place(place_id = 'ChIJSWijB-bH5zsRVLE5ipsxvHU')
pg = str(l)
split = pg.split('=')
print split

q =results.data
print q[2].
#print (results[0])



#address = geocoder.reverse([37.77922,-122.41922], exactly_one=False);
#print address
print results

#Reverse Geocoder using geopy
#Start
geolocator = Nominatim()
location = geolocator.reverse("25.755942, -80.378151")
#print location.address #Returns Full Adress as A string
print location
placeName = location.address.split(',')
print "Printing the name of the place: " + placeName[0]
'''
#Find distance between two points
#Start

#loc1 = (37.7528679,-122.4185353)
##loc2 = (37.7528804, -122.4185364)
#print(great_circle(loc1, loc2).kilometers)
#End

#ChIJCVOWkMeAhYARS9aj9GhYuc8,ChIJ8aZslMeAhYARk2BJNvkVPyc,ChIJr3AblMeAhYARrtrGjPRtH3k


l =google_places.get_place(place_id = 'ChIJ6TRCEUN-j4ARj2bdLZOgsLA')
printable = set(string.printable)
print (filter(lambda x: x in printable, l.name))

#print l.name
#placeName2 = str(l.name.replace("\xce", "n"))
#print placeName2
#try:
#    placeName1 = str(l.name.replace(",", ""))
#except:
    #print "SDSDSD"
    #name = l.name
    #print "dfsdfsdfsd"
#    place = l.name[:-1]
    #print place
#print l.name.split("\\")[0].split("\\x")
#print l.name

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




loc1 = (37.78783, -122.40828)
loc2 = (37.7855, -122.42655)
#print(great_circle(loc1, loc2).kilometers)

#print 'hello'
#result= calculate_initial_compass_bearing(loc1,loc2)
#print result
