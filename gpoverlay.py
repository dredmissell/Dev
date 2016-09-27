import pip
import fiona, os, sys
from shapely.geometry import shape, Polygon
import geopandas as gpd


#############       SUBSETS
#bufSHP = "../TestHPCCData/testbbs_single.shp"
bufSHP = "../TestHPCCData/bbs_sub_Albers.shp"
huc4SHP = "../TestHPCCData/test.shp"
outFile = r"c:\temp\WBDHU4_Albers_out.shp"


#print "reading 4 digit hucs into memory....................."
#huc4SHPPoly = gpd.read_file(huc4SHP)
#print huc4SHPPoly.head(n=1)
print "reading bbs bufferss into memory...................."
#df = gpd.read_file('../TestHPCCData/test.shp')
#df[df['OBJECTID'] == 42].to_file('../TestHPCCData/new_shape.shp')


#test = bufSHPPoly.ix[0].geometry

#print bufSHPPoly.head(n=1)
#bbs = df[bufSHPPoly.geometry.within(huc4SHPPoly)]
##for index, row in bufSHPPoly.iterrows():

#bufDf = gpd.GeoDataFrame(row.reset_index())

# print row['rtestopNo'], row['X_coord'], row['Y_coord']
# buf_with_huc4 = gpd.sjoin(row, huc4SHPPoly, how="inner", op='intersects')
# print buf_with_huc4.HUC4
# print buf_with_huc4.rtestopNo
# print "performing spatial join...................."
#
#
# print "writing output file...................."
#buf_with_huc4.to_file(driver='ESRI Shapefile',filename=o