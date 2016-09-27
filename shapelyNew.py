import fiona
import shapefile
import csv
from shapely.geometry import shape
from shapely.geometry import Polygon
from shapely.geometry import Point
from rtree import index
from shapely.ops import cascaded_union

# hucPolys = [pol for pol in fiona.open('../TestHPCCData/WBDHU4_Albers.shp')]
# bbsPolys = [pol for pol in fiona.open('../TestHPCCData/bbs_buffers_Albers.shp')]
# "../TestHPCCData/testbbs_single.shp"
#
# for i, bbsPoly in enumerate(bbsPolys):
#     bbsShape = shape(bbsPoly['geometry'])
#     # iterate through polygons
#     for j, hucPoly in enumerate(hucPolys):
#         if bbsShape.within(shape(hucPoly['geometry'])):
#             print hucPoly['properties']['HUC4']

# Above does the basic spatial join by iterating over features but can't read entire bbs_buffers_Albers.shp dataset into memory
# ##############################################################################################################################

# this is horribly ineffient
# below stopped working on the 1186 record (out of 162,000)
# with fiona.open('../TestHPCCData/bbs_buffers_Albers.shp', 'r') as input:
# hucPolys = [pol for pol in fiona.open('../TestHPCCData/WBDHU4_Albers.shp')]
# with open('../TestHPCCData/out.csv', 'wb') as csvfile:
#     csvWriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     with fiona.open('../TestHPCCData/testbbs_cross.shp', 'r') as input:
#         for f in input:
#             bbsShape = shape(f['geometry'])
#             # print f['properties']
#             for j, hucPoly in enumerate(hucPolys):
#                     if bbsShape.within(shape(hucPoly['geometry'])):
#                         print hucPoly['properties']['HUC4'] + '_' + f['properties']['rtestopNo']
#                         csvWriter.writerow([str(hucPoly['properties']['HUC4']), str(f['properties']['rtestopNo'])])
# ##############################################################################################################################



idx = index.Index()

print "loading hucs"

huc_sf = shapefile.Reader("../TestHPCCData/WBDHU4_Albers.shp")
huc_shapes = huc_sf.shapes()
huc_points = [q.points for q in huc_shapes]
huc_polygons = [Polygon(q) for q in huc_points]

bbs_sf = shapefile.Reader("C:/PointShapeFile.shp")
bbs_shapes = points_sf.shapes()
bbs_point_coords = [q.points[0] for q in bbs_point_shapes ]
bbs_points = [Point(q.points[0]) for q in bbs_point_shapes ]



print "loading bbs"
bbsPolys = [pol for pol in fiona.open('../TestHPCCData/testbbs_cross2.shp')]

print "done loading"
idx = index.Index()
count = -1
for q in huc_shapes:
    count +=1
    idx.insert(count, q.bbox)

# Populate R-tree index with bounds of grid cells
# print "create index"
# for pos, cell in enumerate(huc_sf):
#     # assuming cell is a shapely object
#     idx.insert(pos, cell.bounds)

print "index complete"
# Loop through each Shapely polygon
for j in idx.intersection(bbs_shapes.bounds):
        # Verify that point is within the polygon itself not just the bounding box
        if bbsPolys[i].within(polygons[j]):
            print "Match found! ",j
            temp=j
            break
print temp # Either the first match found, or None for no matches


print "done"

# # Build a spatial index based on the bounding boxes of the polygons
# print "loading hu4"
# source_polygons_sf = shapefile.Reader('../TestHPCCData/WBDHU4_Albers.shp')
# source_polygon_shapes = source_polygons_sf.shapes()
# source_polygon_points = [q.points for q in source_polygon_shapes]
# source_polygons = [Polygon(q) for q in source_polygon_points]
#
# print "loadng bbs"
# target_points_sf = shapefile.Reader("../TestHPCCData/bbs_buffers_Albers.shp")
# target_point_shapes = target_points_sf.shapes()
# point_coords= [q.points[0] for q in point_shapes ]
# points = [Point(q.points[0]) for q in point_shapes ]
#
# print "done"
# idx = index.Index()
# count = -1
# for q in hu4:
#     count += 1
#     idx.insert(count, q.bbox)
#
#
# with open('../TestHPCCData/out.csv', 'wb') as csvfile:
#     csvWriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#     with fiona.open('../TestHPCCData/testbbs_cross2.shp', 'r') as input:
#         for f in input:
#             bbsShape = shape(f['geometry'])
#             # print f['properties']
#             for j, hucPoly in enumerate(hucPolys):
#                     if bbsShape.within(shape(hucPoly['geometry'])):
#                         print hucPoly['properties']['HUC4'] + '_' + f['properties']['rtestopNo']
#                         csvWriter.writerow([str(hucPoly['properties']['HUC4']), str(f['properties']['rtestopNo'])])