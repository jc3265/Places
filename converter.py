ACCESS_TOKEN = ''

import urllib

#def build_URL(search_text='',types_text=''):
def build_URL(lat,longit):
    base_url = 'https://maps.googleapis.com/maps/api/place/radarsearch/xml?location='     # Can change json to xml to change output type
    latitude = str(lat)
    longitude = str(longit)
    radius = '10'
    radiusString = '&radius='+radius
    typeS = 'all'
    typeString = '&type=' + typeS
    key_string = '&key='+ACCESS_TOKEN                                           # First think after the base_url starts with ? instead of &
    url = base_url+latitude+','+longitude+radiusString+typeString+key_string
    return url
print(build_URL(37.5789,-122.4456))
#print(build_URL(search_text='1200 19th Ave San Francisco'))
