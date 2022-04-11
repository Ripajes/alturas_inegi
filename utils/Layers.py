import geopandas as gpd

def get_original_layer(document):
    pathFile = document.document.path
    polygons = gpd.read_file(pathFile)
    polygons = polygons.to_crs(4326)
    return polygons.to_json(na='null')