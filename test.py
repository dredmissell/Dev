import fiona
from shapely.ops import cascaded_union
from rtree import index


print "load hucs"
hucPolys = [pol for pol in fiona.open('../TestHPCCData/WBDHU4_Albers.shp')]
print "load bbs"
bbsPolys = [pol for pol in fiona.open('../TestHPCCData/testbbs_cross2.shp')]

idx = index.Index()
print "create spatial index"
# Populate R-tree index with bounds of grid cells
for pos, huc in enumerate(hucPolys):
    # assuming cell is a shapely object
    idx.insert(pos, huc.bounds)

print "intersect............"
# Loop through each Shapely polygon
for bb, bbsPoly in enumerate(bbsPolys):
    # Merge cells that have overlapping bounding boxes
    merged_cells = cascaded_union([hucPolys[pos] for bb in idx.intersection(bbsPoly.bounds)])
    # Now do actual intersection
    print bbsPoly.intersection(merged_cells).area