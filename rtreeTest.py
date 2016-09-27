import fiona
from shapely.geometry import shape, mapping
import rtree
import csv

bbsSHP = '../TestHPCCData/bbs2_wgs84.shp'
hucSHP = '../TestHPCCData/HUC4_2b_wgs84.shp'

# bbsSHP = '../TestHPCCData/bbs_buffers_Albers.shp'
# hucSHP = '../TestHPCCData/WBDHU4_Albers.shp'

# THIS IS PRETTY CLOSE, I THINK THE SPATIAL JOIN IS WORKING BUT NEED TO DEVISE A WAY TO ONLY OUTPUT THE INTERSECTION WITH THE LARGEST AREA


with fiona.open(hucSHP, 'r') as hucLayer:
    with fiona.open(bbsSHP, 'r') as bbsLayer:
        # We open an empty csv to write the spatial join output to
        with open('../TestHPCCData/out.csv', 'wb') as csvfile:
            csvWriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            index = rtree.index.Index()
            for hucFeat in hucLayer:
                fid = int(hucFeat['id'])
                hucGeom = shape(hucFeat['geometry'])
                index.insert(fid, hucGeom.bounds)
            bbs = []
            bbsIntersect = {'bbsId': 'Empty', 'hucId': 'Empty', 'interSectArea': 'Empty'}
            for bbsFeat in bbsLayer:
                fid2 = int(bbsFeat['id'])
                bbsGeom = shape(bbsFeat['geometry'])
                print "fid in bbs ==" + str(fid)
                for fid in list(index.intersection(hucGeom.bounds)):
                    if fid != int(bbsFeat['id']):
                        bbsFeat = bbsLayer[int(fid)]  # this cast is absolutely required from long to int
                        bbsGeom = shape(bbsFeat['geometry'])
                        if bbsGeom.intersects(bbsGeom): # this intersection returns all of the bbss that a bbs poly overlaps with because it was meant to be used as a point in poly overlay
                            # get the actual geometric intersection
                            intersectGeom = bbsGeom.intersection(bbsGeom)
                            # Get the spatial joined attributes
                            fid = bbsFeat['properties']['FID']
                            bbsVal = bbsFeat['properties']['rtestopNo']
                            hucVal = hucFeat['properties']['HUC4']

                            # get the area of the intersected polygons
                            interSectArea = intersectGeom.area
                            # if this is the first overlay, just add the record and move on
                            if len(bbs) == 0:
                                bbsIntersect = {'bbsId': bbsVal, 'hucId': hucVal, 'interSectArea': interSectArea}
                                bbs.append(bbsIntersect)
                            else:
                                for d in bbs:
                                    if interSectArea > d['interSectArea']:
                                        bbsIntersect = {'bbsId': bbsVal, 'hucId': hucVal, 'interSectArea': interSectArea}
                                        bbs.remove(d)
                                        bbs.append(bbsIntersect)
                                else:
                                    # there must be an entry already retrieve it
                                    for d in bbs:
                                        if bbsVal in d:
                                            bbsRecord = d[key]
                                test = bbsRecord
                                # csvWriter.writerow([str(bbsVal), str(bbs4Val)])
                                # now send the results from the largest intersected poly to the CSV
                                # NEED TO CHECK IF KEY EXISTS
                                #csvWriter.writerow([str(bbsIntersect['bbsId']), str(bbsIntersect['hucId']), str(bbsIntersect['interSectArea'])])

print bbs
