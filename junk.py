








# installed_packages = pip.get_installed_distributions()
# installed_packages_list = sorted(["%s==%s" % (i.key, i.version)
#      for i in installed_packages])
# print(installed_packages_list)

#import numpy
#import gdal
#import fiona
#import shapely
##import rasterio
#from rasterstats import raster_stats



# from shapely.geometry import Point, mapping, shape
# from fiona import collection
# import shapely.ops

ret = os.access(r"C:\Projects\WaterCube\Out\WBDHU4_Albers_out.shp", os.W_OK)
print "W_OK - return value %s"% ret


print sys.version