from pyproj import Proj, transform

P3857 = Proj(init='epsg:3857')
P4326 = Proj(init='epsg:4326')
lon=-122.3568
lat=37.48
x,y = transform(P3857, P4326, lon, lat)

print  x
print  y
