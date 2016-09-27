# ###################################################################################################################
# Name:             RasterOverlay.py
# Purpose:          Raster STats
# Requirements:     Polygon Zones shaps and rasters
# Date:             09/19/2016
# Author:           Ed Bissell, RS&GIS
# Documentation:    <Watercube_SpatialAnalysis_Documentation.docx>
######################################################################################################################
#

import os
import fiona
from shapely.geometry import shape
from osgeo import osr, gdal, gdalconst
import rasterstats
from pprint import pprint
from rasterstats import zonal_stats
# import pydem
#from pydem.dem_processing import DEMProcessor
#
#rasterpath = '../TestHPCCData/rasterTest/bio02_Albers.tif'
#shppath = '../TestHPCCData/Test/HUC4.shp'  # 2 poly subset
# shppath = '../TestHPCCData/WBDHU4_Albers.shp'
#
#stats = zonal_stats(shppath, rasterpath, stats = "mean")
#pprint(stats)

#alltouched
#[{'__fid__': 0, 'mean': 11.21263670295833},
 #{'__fid__': 1, 'mean': 11.112216664529313}]



# test categorical raster here
# catstats = zonal_stats('../TestHPCCData/Test/HUC4.shp', '../TestHPCCData/rasterTest/nlcd_subset.tif', categorical=True)
# pprint(catstats)


# rasterpath = '../TestHPCCData/smallRasterTest/bio02_Albers3.tif'
#smallshppath = '../TestHPCCData/smallRasterTest/IWS14165.shp'  # 2 poly subset
# smallshppath = '../TestHPCCData/smallRasterTest/IWS6906.shp'
# stats = zonal_stats(smallshppath, rasterpath)
# pprint(stats)

# imgpath = 'C:\Projects\WaterCube\TestHPCCData\NEDIMG_test\USGS_NED_1_n42w086_IMG\USGS_NED_1_n42w086_IMG_Albers.img'
#
# shppath = 'C:\Projects\WaterCube\TestHPCCData\smallRasterTest\IWS_42_86.shp'
# stats2 = zonal_stats(shppath, imgpath)
# pprint(stats2)
inpath = 'C:/Temp/ned7'
for raster in (os.path)
imgpath = 'C:/Projects/WaterCube/TestHPCCData/NEDIMG_test/USGS_NED_1_n42w086_IMG/USGS_NED_1_n42w086_IMG_Albersfel.img'
inpath = 'C:/Temp/ned7/USGS_NED_1_n42w085_IMG.tif'
outpath = 'C:/Temp/ned7/slopepython4.tif'
os.system("gdaldem slope -p -alg ZevenbergenThorne -compute_edges -of GTiff " + inpath + " " +  outpath)