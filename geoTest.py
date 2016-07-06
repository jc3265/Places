from pygeocoder import Geocoder
from googleplaces import GooglePlaces
import geocoder
import csv

#results = Geocoder(api_key='AIzaSyDYElSVqyQ9lUg9ksctNXg8JiSj_6-hEVU')
'''
with open('/home/zrtho/Documents/csvFilesWithTimeStamp/pyTest.csv', 'rb') as csvfile:
    myFile = csv.reader(csvfile, delimiter=',')
    for row in myFile:
        tid = int(row[0])
        latitude = float(row[1])
        longitude = float(row[2])
        occupancy = int(row[3])
        time = row[4]
        gid = row[5]
        results = Geocoder.reverse_geocode(latitude,longitude)
        print (results[0])
'''
#results = Geocoder(api_key='AIzaSyDYElSVqyQ9lUg9ksctNXg8JiSj_6-hEVU').reverse_geocode(25.756990, -80.379611)

#results = Geocoder.geocode("Tian'anmen, Beijing")
results = Geocoder.reverse_geocode(37.77922,-122.41922)
#print (results[0])
#test = Geocoder.geocode("1 Dr Carlton B godlett p1, San Francisco")
q = geocoder.google([37.77922,-122.41922], method='reverse')
place = q


p=GooglePlaces('AIzaSyDYElSVqyQ9lUg9ksctNXg8JiSj_6-hEVU').get_place(q.place)
print p.details

'''
print h[0]
#print test
print (results[0])
#print (test[0])

'''
