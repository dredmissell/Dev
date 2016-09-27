from shapely.geometry import mapping, shape
from shapely.ops import cascaded_union
from fiona import collection
bufSHP = "../TestHPCCData/testbbs_single.shp"
huc4SHP = "../TestHPCCData/test.shp"
with collection("../TestHPCCData/test.shp", "r") as input:
    schema = input.schema.copy()
    with collection(
            "../TestHPCCData/testbbs_single.shp", "w", "ESRI Shapefile", schema) as output:
        shapes = []
        for f in input:
            shapes.append(shape(f['geometry']))
        merged = cascaded_union(shapes)
        output.write({
            'properties': {
                'name': 'Buffer Area'
                },
            'geometry': mapping(merged)
            })