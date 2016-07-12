from googleplaces import GooglePlaces, types, lang
from pygeocoder import Geocoder
from geopy.geocoders import Nominatim
from geopy.distance import great_circle
import geocoder
import csv


Key = 'AIzaSyDYElSVqyQ9lUg9ksctNXg8JiSj_6-hEVU'
google_places = GooglePlaces(Key)
'''
l =google_places.get_place(place_id = 'ChIJSWijB-bH5zsRVLE5ipsxvHU')
pg = str(l)
split = pg.split('=')
print split

results = Geocoder.reverse_geocode(37.77922,-122.41922)
q =results.data
print q[2].
#print (results[0])


#results = geocoder.google([37.77922,-122.41922], method='reverse')
#address = geocoder.reverse([37.77922,-122.41922], exactly_one=False);
#print address


#Reverse Geocoder using geopy
#Start
geolocator = Nominatim()
location = geolocator.reverse("25.755942, -80.378151")
#print location.address #Returns Full Adress as A string
print location
placeName = location.address.split(',')
print "Printing the name of the place: " + placeName[0]

#Find distance between two points
#Start
loc1 = (37.77922,-122.41922)
loc2 = (41.49008, -71.312796)
print(great_circle(loc1, loc2).kilometers)
#End
'''


l =google_places.get_place(place_id = 'ChIJK6WIhNVTqEcRskAq8CGZva0')
print l.details
