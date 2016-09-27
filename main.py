import geopandas as gpd
import fiona

#############       subsets
bufSHP = "../TestHPCCData/bbs_sub_Albers.shp"
#bufSHP = "../TestHPCCData/testbbs_single.shp"
huc4SHP = "../TestHPCCData/test.shp"

#############       all features
# bufSHP = "../TestHPCCData/bbs_buffers_Albers.shp"
huc4SHP = "../TestHPCCData/WBDHU4_Albers.shp"
test = "../TestHPCCData/test.shp"

outFile = "../Out/WBDHU4_Albers_out.shp"
#outFile = r"c:\temp\WBDHU4_Albers_out.shp"

# schema = fiona.open(huc4SHP).schema
# fiona
polybuf = [pol for pol in fiona.open('../TestHPCCData/WBDHU4_Albers.shp')]
polyhuc = [pol for pol in fiona.open('../TestHPCCData/WBDHU4_Albers.shp')]
print "performing spatial join...................."
bufSHPPoly = gpd.read_file(test)
huc4SHPPoly = gpd.read_file(huc4SHP)
buf_with_huc4 = gpd.sjoin(huc4SHPPoly, bufSHPPoly, how="inner", op='intersects')
print "writing output file...................."
buf_with_huc4.to_file(driver='ESRI Shapefile',filename=outFile)
print "done!"
# for poly in polybuf:
#     newDf = gpd.GeoDataFrame(poly.geometry)
#     buf_with_huc4 = gpd.sjoin(poly[0].geometry, polyhuc, how="inner", op='intersects')
#     print buf_with_huc4.HUC4
#     print buf_with_huc4.rtestopNo
    # print(poly['properties'])
#
# print "reading 4 digit hucs into memory....................."
# huc4SHPPoly = gpd.read_file(huc4SHP)
# # print huc4SHPPoly.head(n=1)
# print "reading bbs bufferss into memory...................."
# bufSHPPoly = gpd.read_file('../TestHPCCData/testbbs_single.shp')
# # print bufSHPPoly.head(n=1)
# # bbs = df[bufSHPPoly.geometry.within(huc4SHPPoly)]
# for index, row in bufSHPPoly.iterrows():
#     print row['rtestopNo'], row['X_coord'], row['Y_coord']
#     buf_with_huc4 = gpd.sjoin(row.geometry, huc4SHPPoly, how="inner", op='intersects')
#     print buf_with_huc4.HUC4
#     print buf_with_huc4.rtestopNo

#

# # print buf_with_huc4.columns




# the join is working just need to get just the right columns out -- BBS_rout_4 I think is the uid & HUC4
# produces bad
#print "finished...................."


# with fiona.open(outPath, 'w', 'ESRI Shapefile', schema) as output:
#     for poly in polygons:
#         print(poly['properties'])
#         #output.write(poly)





# with collection(bufSHP, "r") as input:
#     schema = input.schema.copy()
#     with collection(huc4SHP, "w", "ESRI Shapefile", schema) as output:
#         shapes = []
#         for f in input:
#             shapes.append(shape(f['geometry']))
#         merged = shapes.intersection(ctSHP)
#         output.write({
#             'properties': {
#                 'uid': point['properties']['uid']
#                 },
#             'geometry': mapping(merged)
#             })

# print "test"
#
# stats = raster_stats("../TestHPCCData/bbs_sub_Albers.shp", "../TestHPCCData/us_ppt_1970012sub.tif",stats = ['min', 'max', 'median', 'majority', 'sum'],  copy_properties=True)
# print stats[1].keys()

# for n in stats:
#    for rtestopNo, max in n:
#        print '{0} corresponds to {1}'.format(rtestopNo, max)
# if n['rtestopNo']:
#     print n
# print stats
