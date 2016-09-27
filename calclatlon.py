import fiona
from shapely.geometry import shape, mapping, Polygon, MultiPolygon
import rtree
import csv
import os

from pyproj import Proj, transform
import fiona
from fiona.crs import from_epsg

# DEV
#targetSHP = '../TestHPCCData/Test/bbs.shp'
targetSHP = '../TestHPCCData/bbs_buffers_Albers.shp'


outPath = '../TestHPCCData/Out'

def calclatlon(target, targetid):
    with open(outPath + '/Out' + target + 'latlon' + '.csv', 'wb') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csvWriter.writerow([targetid, 'long', 'lat'])
        print "Opening target shapefile ........."
        with fiona.open(targetSHP, 'r') as targetLayer:
            original = Proj(targetLayer.crs)  # source EPSG
            destination = Proj(init='EPSG:4326')  # your new EPSG
            for targetFeat in targetLayer:
                targetGeom = shape(targetFeat['geometry'])
                targetIdVal = targetFeat['properties'][targetid]
                print "Calculating lat/lon for id: " + targetIdVal + " -------------------- "
                # need to deal with multi-polygon issue here
                if targetIdVal == '2013-20':
                    test = targetIdVal
                #poly = Polygon(targetGeom)
                #print poly.geom_type
                x, y = targetGeom.centroid.xy
                long, lat = transform(original, destination, x, y)
                # spit out the lat/lons
                csvWriter.writerow([str(targetIdVal), str(long[0]), str(lat[0])])


#calclatlon('bbs', 'rtestopNo')

# calc larger HUCS from 12 digit HUCs rather than re-overlaying
def calchucs(dir):
    with (open(dir + '/' + 'OutHUC12.csv', 'r')) as infile:
        with (open(dir + '/' + 'OutHUC4_8_12.csv', 'w')) as outfile:
            outfieldnames = ['rtestopno', 'HUC4', 'HUC8', 'HUC12']
            reader = csv.DictReader(infile)
            writer = csv.writer(outfile)
            writer.writerow(['rtestopno','HUC4','HUC8','HUC12'])
            for row in reader:
                id = row['rtestopno']
                HUC12 = row['HUC12']
                HUC4 = row['HUC12'][:4]
                HUC8 = row['HUC12'][:8]
                print "Calcing HUCS for " + id + "-------------"
                writer.writerow([str(id), str(HUC4), str(HUC8), str(HUC12)])

#calchucs(outPath)

