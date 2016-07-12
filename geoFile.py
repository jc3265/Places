#!/usr/bin/env python
#import urllib      ##libary to for the build url function Not used
import csv         #Csv library
import requests    #Url Requests library
import re          #Return Library
Key = 'AIzaSyDYElSVqyQ9lUg9ksctNXg8JiSj_6-hEVU'

####################################################################################
#Create Function that looks for the nearby places of a given latitude and longitude#
####################################################################################
def build_URL(lat,longit):
    base_url = 'https://maps.googleapis.com/maps/api/place/radarsearch/json?location='     # Can change json to xml to change output type
    lat = str(lat) #Cast String to the Float
    longit = str(longit) #Cast String to the Float
    radius = '10'   #Radius of search in meters
    radiusString = '&radius='+radius
    typeS = 'all' #types, can be specific such as church, park, gas station, etc...
    typeString = '&type=' + typeS
    key_string = '&key='+Key
    url = base_url+latitude+','+longitude+radiusString+typeString+key_string
    return url

with open('/home/zrtho/Documents/csvFilesWithTimeStamp/place.csv', 'rb') as csvfile:
    myFile = csv.reader(csvfile, delimiter=',')
    for row in myFile:
        tid = int(row[0])
        latitude = row[1]
        longitude = row[2]
        occupancy = int(row[3])
        time = row[4]
        gid = row[5]
        urlResult= build_URL(latitude,longitude)
        req = requests.get(urlResult)
        oneLine = str(req.json())
        someT = re.findall(r'place_id', oneLine)[0]
        print someT
