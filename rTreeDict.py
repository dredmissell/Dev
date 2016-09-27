# ###################################################################################################################
# Name:             BBSSpatialJoin.py
# Purpose:          Overlay BBS with HUCS & LAGOS Sheds
# Requirements:     BBS, HUC12, LAGOS Sheds in valid coord system, etc....
# Date:             09/15/2016
# Author:           Ed Bissell, RS&GIS
# Documentation:    <Watercube_SpatialAnalysis_Documentation.docx>
######################################################################################################################
#

import fiona
from shapely.geometry import shape
import rtree
import csv
from pyproj import Proj, transform

outPath = '../TestHPCCData/Out'
stage = 'Prod' # 'Test'

# DEV
#targetSHP = '../TestHPCCData/Test/bbs.shp'
#huc4SHP = '../TestHPCCData/HUC4_2b.shp'

# PROD
targetSHP = '../TestHPCCData/bbs_buffers_Albers.shp'

def _get_by_id(vals, targetId):
    return next(x for x in vals if x['targetId'] == targetId)

def _get_by_id2(vals, targetId):
    return next(x for x in vals if x['rtestopno'] == targetId)

def spatialjoin(targetid, joinsource, joinid):
    target = []
    #for prod/dev add remove Test directory
    joinSHP = '../TestHPCCData/' + stage + '/' + joinsource + '.shp'
    targetIntersect = {'targetId': 'rtestopno', 'joinId': joinid, 'interSectArea': 'intersectArea'}
    target.append(targetIntersect)
    print "Opening join Shapefile........."
    with fiona.open(joinSHP, 'r') as joinLayer:

        print "Opening target shapefile ........."
        with fiona.open(targetSHP, 'r') as targetLayer:
            index = rtree.index.Index()
            for joinFeat in joinLayer:
                fid = int(joinFeat['id'])
                joinGeom = shape(joinFeat['geometry'])
                index.insert(fid, joinGeom.bounds)
            for targetFeat in targetLayer:
                targetGeom = shape(targetFeat['geometry'])
                print "--------------"
                print "intersecting target " + targetFeat['properties'][targetid]
                for fid in list(index.intersection(targetGeom.bounds)):
                # if fid != int(targetFeat['id']):
                    joinFeat = joinLayer[int(fid)]  # this cast is absolutely required from long to int
                    joinGeom = shape(joinFeat['geometry'])
                    if joinGeom.intersects(targetGeom): # this intersection returns all of the joins that a target poly overlaps with
                        # get the actual geometric intersection
                        intersectGeom = targetGeom.intersection(joinGeom)
                        # Get the spatially joined attributes
                        targetIdVal = targetFeat['properties'][targetid]
                        joinIdVal = joinFeat['properties'][joinid]
                        # get the area of the intersected polygons
                        interSectArea = intersectGeom.area
                        # add the attributes for the current poly to a dictionary
                        targetIntersect = {'targetId': targetIdVal, 'joinId': joinIdVal, 'interSectArea': interSectArea}
                        print "this intersected +++++++++" + str(targetIntersect)
                        my_item = None
                        for dictitem in target:
                            if dictitem['targetId'] == targetIdVal:
                                my_item = dictitem
                                break
                            else:
                                my_item = None
                        if my_item is not None:
                            test = my_item
                            curdict = _get_by_id(target, targetIdVal)
                            for dictitem in target:
                                if dictitem['targetId'] == targetIdVal:
                                    if interSectArea > dictitem['interSectArea']:
                                        dictitem['joinId'] = joinIdVal
                                        dictitem['interSectArea'] = interSectArea
                        else:
                            target.append(targetIntersect)
    # just sort for testing purposes
    #newtarget = sorted(target, key=lambda k: k['targetId'])
    with open(outPath + '/Out' + joinsource + '.csv', 'wb') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for d in target:
            #csvWriter.writerow([str(d['targetId']), str(d['joinId']), str(d['interSectArea'])])
            csvWriter.writerow([str(d['targetId']), str(d['joinId'])])
    #print target

# Usage: spatialjoin(<targetid>, <joinsource>, <joinid>)
# targetid = unique identifier of the target dataset
# joinsource = shapefile that has the attribute to join
# joinid = attribute from the joinsource to join to the target
#spatialjoin('rtestopNo', 'HUC12', 'HUC12')
#spatialjoin('rtestopNo', 'IWS', 'lagoslakei')


# Take previously processed CSV files and merge into 1 file
# Currently hardcode to work with BBS PK
def mergecsv(dir):
    flist = []
    with open(outPath + '/Outbbslatlon.csv', 'r') as infile1:
        csvreader1 = csv.DictReader(infile1)
        for row1 in csvreader1:
            #next(csvreader1, None)  # skip the headers
            id1 = row1['rtestopno']
            print 'Processing ' + id1 + " for lat/lon"
            long = row1['long']
            lat = row1['lat']
            fout1 = {'rtestopno': id1, 'long': long, 'lat': lat, 'HUC4': '', 'HUC8': '', 'HUC12': ''}
            flist.append(fout1)
        print "Finished adding entries to dictionary"
        with open(outPath + '/OutHUC4_8_12.csv', 'r') as infile2:
            csvreader2 = csv.DictReader(infile2)
            for row2 in csvreader2:
                #next(csvreader2, None)  # skip the headers
                id2 = row2['rtestopno']
                print 'Processing ' + id2 + " for HUCS"
                HUC4 = row2['HUC4']
                HUC8 = row2['HUC8']
                HUC12 = row2['HUC12']
                curdict = _get_by_id2(flist, id2)
                curdict['HUC4'] = HUC4
                curdict['HUC8'] = HUC8
                curdict['HUC12'] = HUC12
            print "Finished populating HUCs"
            with open(outPath + '/OutIWS.csv', 'r') as infile3:
                csvreader3 = csv.DictReader(infile3)
                for row3 in csvreader3:
                    #next(csvreader3, None)  # skip the headers
                    id3 = row3['rtestopno']
                    print 'Processing ' + id3 + " for lagoslakei"
                    lagoslakei = row3['lagoslakei']
                    curdict = _get_by_id2(flist, id3)
                    curdict['lagoslakei'] = lagoslakei
    print "Finished populating lagoslakeid. Now outputting CSV"
    with open(outPath + '/BBS_SpatialJoin_Merge.csv', 'wb') as csvfile:
        csvWriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        csvWriter.writerow(['rtestopNo', 'lon', 'lat','HUC4', 'HUC8', 'HUC12','lagoslakeid']) # write the header row
        for d in flist:
            if d.has_key('lagoslakei'):
                csvWriter.writerow([str(d['rtestopno']), str(d['long']), str(d['lat']), str(d['HUC4']), str(d['HUC8']), str(d['HUC12']), str(d['lagoslakei'])])
            else:
                csvWriter.writerow([str(d['rtestopno']), str(d['long']), str(d['lat']), str(d['HUC4']), str(d['HUC8']), str(d['HUC12']), str('')])

mergecsv(outPath)

#Remove rows for BBS polys in Alaska, not technically part of study extent
def purge(dir):
    with open(dir + '/BBS_SpatialJoin_Merge.csv', 'r') as infile:
        with open(dir + '/BBS_SpatialJoin_Final.csv', 'wb') as outfile:
            csvreader = csv.DictReader(infile)
            csvWriter = csv.writer(outfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            csvWriter.writerow(['rtestopNo', 'lon', 'lat', 'HUC4', 'HUC8', 'HUC12', 'lagoslakeid'])  # write the header row
            #next(csvreader, None)  # skip the headers
            for row in csvreader:
                if row['HUC4'] != ""''"": # only need to check for HUC4 being empty
                    csvWriter.writerow([str(row['rtestopNo']), str(row['lon']), str(row['lat']), str(row['HUC4']), str(row['HUC8']), str(row['HUC12']),str(row['lagoslakeid'])])
#purge(outPath)

# Usage: calclatlon(<target>, <targetid>)
# target - shapefile to calc coordinates for
# targetid - unique identifier of dataset
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
                x, y = targetGeom.centroid.xy
                long, lat = transform(original, destination, x, y)
                # spit out the lat/lons
                csvWriter.writerow([str(targetIdVal), str(long[0]), str(lat[0])])


#calclatlon('bbs', 'rtestopNo')

# calc larger HUCS from 12 digit HUCs rather than re-overlaying
# Usage: calchucs(<dir>)
# dir = location of output directory
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
