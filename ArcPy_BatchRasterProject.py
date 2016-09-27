# ###################################################################################################################
# Name:             ArcPy_BatchRasterProject.py
# Purpose:          Project a directory of rasters to new coordinate system and saves results as GEOTiff
# Requirements:     directory of rasters where the actual raster file is buried within a subdirectory and uses the
#                   same naming pattern as the raster
#                   Downloaded NED tiles as IMG from ftp://rockyftp.cr.usgs.gov/vdelivery/Datasets/Staged/Elevation/1/IMG/
#                   Could not project these directly as the coordinate system was undefined so used this workflow
#                   1) Unzip all archives using 7-Zip
#                   2) Run 1st part of script to convert/copy all .imgs to one directory
#                   3) Second part of script projects to USGS Albers
# Date:             09/282016
# Author:           Ed Bissell, RS&GIS
######################################################################################################################
#Has not been tested on all NED at once, may want to subset apriori

import arcpy
import os

# path to extracted rasters
unzippedpath = r'C:/Temp/ned3'
rasterpath = r'C:/Temp/ned6'
projectedpath = r'C:/temp/ned7'
outsr = arcpy.SpatialReference(5070) # USA Albers CONUS

# convert IMGS to TIFF and transfer to a new directory
rasters = []
for dirpath, subdirs, files in os.walk(unzippedpath):
    for name in files:
        if name.endswith('.img'):
            rasters.append(os.path.join(dirpath, name))
arcpy.AddMessage("Converting Rasters.................")
arcpy.RasterToOtherFormat_conversion(rasters, rasterpath, "TIFF")
arcpy.AddMessage("Raster Conversion Complete!!!")

arcpy.env.workspace = rasterpath

# iterate over tiffs and project to USGS Albers
for raster in arcpy.ListRasters():
    arcpy.AddMessage("Projecting " + raster + " ....................")
    arcpy.ProjectRaster_management(rasterpath + os.sep + raster, projectedpath + os.sep + raster, outsr, "BILINEAR", "30")
    arcpy.AddMessage("Projecting " + raster + " complete")
arcpy.AddMessage("Projecting complete" + " !!!")



