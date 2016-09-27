# open source spatial join script
# fiona and shapely scripting adapted from ThomasG77's comment from:
# http://gis.stackexchange.com/questions/119374/intersect-shapefiles-using-shapely
#

# import libraries
import fiona, rtree, os, shapefile
from shapely.geometry import shape, mapping
from os.path import isfile

# select input files with nicely extendible input options :D
print "Please enter directory containing shapefiles (also for output):"
print "Example: /Users/samuelestabrook/Desktop/spatial_join_test/"
shapeSpace = raw_input('Enter directory ')
listShapes = [f for f in os.listdir(shapeSpace) if f.endswith('.shp')]
for listShape in listShapes:
    printData = '{0}'.format(listShape)
    print printData
print "Please copy the names plus extensions of the two files needed for the joing:"
print "Example: Study_area_extent.shp"
pointSHP = '{0}/{1}'.format(shapeSpace, raw_input('Name of point file to be attributed '))
polySHP = '{0}/{1}'.format(shapeSpace, raw_input('Name of polygon file for spatial join '))

# select field from polygons for join
reader = shapefile.Reader(polySHP)
fields = reader.fields[1:]
print '{0}'.format(fields)
print "Please copy the field needed of the attribute to join to points:"
print "Example: FIPS_code"
polyAtt = raw_input('Enter field name for polygon attribute ')

# name field for joined attribute
print "Please create a field name for the new points attribute:"
print "Example: joined_att"
joinAtt = raw_input('Create field name for new points attribute ')

# some fancy result output handling :D :D
sequence = ""
filename = "result%s.shp"
while isfile(filename % sequence):
    sequence = int(sequence or "0") + 1
filename = filename % sequence
resultSHP = '{0}/{1}'.format(shapeSpace, filename)

# open polygon shapefile as read only
with fiona.open(polySHP, 'r') as layer1:
    # open point shapefile as read only
    with fiona.open(pointSHP, 'r') as layer2:
        # copy point schema and add the new attribute for the new resulting point shapefile
        schema = layer2.schema.copy()
        schema['properties'][joinAtt] = 'int:10'
        # open an empty shp to write the points with the polygon attribute
        with fiona.open(resultSHP, 'w', 'ESRI Shapefile', schema) as layer3:
            # create index to reduce query load
            index = rtree.index.Index()
            # loop through the polygons to index their bounds
            for feat1 in layer1:
                # use id to identify polygon index key
                fid = int(feat1['id'])
                # pull in geometry
                geom1 = shape(feat1['geometry'])
                # add to index
                index.insert(fid, geom1.bounds)
            # loop through each point
            for feat2 in layer2:
                # pull in geometry
                geom2 = shape(feat2['geometry'])
                print "Point", feat2
                # loop through intersecting polygon index results
                for fid in list(index.intersection(geom2.bounds)):
                    # some sort of error control ????
                    if fid != int(feat2['id']):
                        # pull the polygon shapes into the loop for intersection
                        feat1 = layer1[fid]
                        try:
                            # geom1 = shape(feat1['geometry'])
                            # loop to find the intersecting polygon from the index results
                            if geom1.intersects(geom2):
                                # take attributes from the polygon
                                prop1 = feat2['properties']
                                # append the join_att attribute we want from the polygon
                                prop1[joinAtt] = feat1['properties'][polyAtt]
                                # write the properties and geometry in the new point shapefile
                                layer3.write({
                                    'properties': prop1,
                                    'geometry': mapping(geom2)
                                })
                        except TypeError:
                            print "Some kinda geometry error"