from pygeocoder import Geocoder
from googleplaces import GooglePlaces
# from geopy.geocoders import Nominatim  # osm
from geopy.geocoders import *
import geocoder
import csv
import datetime
#results = Geocoder(api_key='AIzaSyDYElSVqyQ9lUg9ksctNXg8JiSj_6-hEVU')

Key = 'AIzaSyDYElSVqyQ9lUg9ksctNXg8JiSj_6-hEVU'

google_places = GooglePlaces(Key)

geolocator = Nominatim() #osm Returns an object
#with open('/home/zrtho/Documents/new_abboip.csv', 'rb') as csvfile:
#geolocator = GoogleV3(api_key='AIzaSyDYElSVqyQ9lUg9ksctNXg8JiSj_6-hEVU') # .reverse returns a list of size 8

with open('/home/zrtho/Documents/csvFilesWithTimeStamp/place.csv', 'rb') as csvfile:
    myFile = csv.reader(csvfile, delimiter=',')
    for row in myFile:
        tid = int(row[0])
        latitude = float(row[1])
        longitude = float(row[2])
        occupancy = int(row[3])
        time = str(row[4])
        #time = str(row[4]).replace("-", " ")
        someTime = '05-17-2008 06:08:23'
        dateS = datetime.datetime.strptime(str(someTime), '%m-%d-%Y %H:%M:%S') # Read the time
        dateSD = datetime.datetime.strptime(time, '%m-%d-%Y %H:%M:%S') # Read the time
        gid = row[5]
        timediff = dateS - dateSD
        distance = 1000
        print distance/timediff.total_seconds()
        ##Using geopy
        #location = geolocator.reverse([latitude,longitude])
        #placeName = location.address.split(',')
        #print "\nPrinting the name of the place: " + placeName[0]
        #print "Full Info"
        #print location.name
        #print "Lat"
        #print latitude
        #print "Long"
        #print  longitude

        ##End

        ###Using geocoder
        #results = geocoder.google([latitude,longitude], method='reverse') # Returns a geocoder object
        #results = Geocoder.reverse_geocode(latitude, longitude)
        #print 'Results'
        #print results.address.split(',')[0]
        #print results

        #print geocoder.google([latitude,longitude], method='reverse').geojson
        #p=GooglePlaces('AIzaSyDYElSVqyQ9lUg9ksctNXg8JiSj_6-hEVU').get_place(results.place)
        #print p.details
        #details= google_places.get_place(place_id = results)
        #details = str(details)
        #print "details: " + details
        #placeName = details.split('"')
        #print (placeName[1])


'''
#results = Geocoder(api_key='AIzaSyDYElSVqyQ9lUg9ksctNXg8JiSj_6-hEVU').reverse_geocode(25.756990, -80.379611)

#results = Geocoder.geocode("Tian'anmen, Beijing")
results = Geocoder.reverse_geocode(37.77922,-122.41922)
#print (results[0])
#test = Geocoder.geocode("1 Dr Carlton B godlett p1, San Francisco")
q = -geocoder.google([37.77922,-122.41922], method='reverse')
place = q
print "Json"
placeID= q.place

print "GeoJson"
print q.geojson.viewvalues


p=GooglePlaces('AIzaSyDYElSVqyQ9lUg9ksctNXg8JiSj_6-hEVU').get_place(q.place)
#print p.details
print h[0]
#print test
print (results[0])
#print (test[0])

'''
