# read the shapefiles
import fiona
from shapely.geometry import shape
from shapely.ops import cascaded_union
from rtree import index
bufSHP = "../TestHPCCData/testbbs_single.shp"
huc4SHP = "../TestHPCCData/test.shp"
polygons = [pol for pol in fiona.open('../TestHPCCData/test.shp')]
points = [pt for pt in fiona.open('../TestHPCCData/testbbs_single.shp')]
# attributes of the polygons
for poly in polygons:
    print poly['properties']


# attributes of the points
for pt in points:
    print pt['properties']


idx = index.Index()
for pos, poly in enumerate(polygons):
    idx.insert(pos, shape(poly['geometry']).bounds)

# Loop through each Shapely polygon
for poly in polygons:
    # Merge cells that have overlapping bounding boxes
    merged_cells = cascaded_union([grid_cells[pos] for pos in idx.intersection(poly.bounds)])
    # Now do actual intersection
    print poly.intersection(merged_cells).area