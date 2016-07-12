#!/usr/bin/env python
#import urllib      ##libary to for the build url function Not used
import csv         #Csv library
import requests    #Url Requests library
import re          #Return Library
Key = 'AIzaSyDYElSVqyQ9lUg9ksctNXg8JiSj_6-hEVU'
myTextFile = '/home/zrtho/Documents/pythonTest/output1.txt'

####################################################################################
#   Function that looks for the nearby places of a given latitude and longitude    #
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

#####################################################
#   Function that Writes the result in json format  #
#####################################################
def writeToFile(url):
    text_file = open(myTextFile, "w")#Text file where the output will be stored
    #text_file.write(str(requests.get(urlResult).text) #Prints nicely in text format
    text_file.write(str(requests.get(urlResult).json()))
    text_file.close() #close file so that every line is a new file


def checkTheFile():
    fileToRead = open(myTextFile,"r")#Read the same file and scan for a string
    for line in fileToRead:
        if 'place_id' in line:
            #print "found"
            #print line.split('place_id')[1]
            place_id = line.split('place_id')[1].replace("',","u'").split("u'")[1]
            return place_id
        else:
            #print "Not Found"
            return "Road"
        #print tid
    fileToRead.close()


with open('/home/zrtho/Documents/csvFilesWithTimeStamp/place.csv', 'rb') as csvfile:
    myCsvFile = csv.reader(csvfile, delimiter=',')
    for row in myCsvFile:
        #text_file = open('/home/zrtho/Documents/pythonTest/output1.txt', "w")#Text file where the output will be stored
        tid = int(row[0])
        latitude = row[1]
        longitude = row[2]
        occupancy = int(row[3])
        time = row[4]
        gid = row[5]
        urlResult= build_URL(latitude,longitude)
        writeToFile(urlResult)
        place_id = checkTheFile()
        print place_id
        #with open('fileToRead', 'r')


#        print req.startswith('place_id')
'''
        someT = re.findall(r'place_id', oneLine)
        print someT[0]
        print len(someT)
        if()
'''
