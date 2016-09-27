import fiona
from shapely.geometry import Polygon, Point
from rtree import index

from shapely.geometry import shape
polygons = [pol for pol in fiona.open('../TestHPCCData/test.shp')]

# List of non-overlapping polygons
# polygons = [
#     Polygon([(0, 0), (0, 1), (1, 1), (0, 0)]),
#     Polygon([(0, 0), (1, 0), (1, 1), (0, 0)]),
# ]

# Populate R-tree index with bounds of polygons
idx = index.Index()
for pos, poly in enumerate(polygons[0]):
    idx.insert(pos, poly.bounds)

# Query a point to see which polygon it is in
# using first Rtree index, then Shapely geometry's within
# point = Point(0.5, 0.2)
# poly = Polygon([(0, 0), (0, 1), (1, 1), (0, 0)])
poly = [pol for pol in fiona.open('../TestHPCCData/testbbs_single.shp')]
poly_idx = [i for i in idx.intersection(poly[0].bounds)
            if poly.within(polygons[i])]
for num, idx in enumerate(poly_idx, 1):
    print("%d:%d:%s" % (num, idx, polygons[idx]))