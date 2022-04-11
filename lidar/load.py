from pathlib import Path
from django.contrib.gis.utils import LayerMapping
from lidar.models import LidarBorder

lidar_mapping = {
    'clave10k':'clave10k',
    'geom': 'MULTIPOLYGON',
}

lidar_shape = Path(__file__).resolve().parent / 'data' / 'cartas.shp'

def run(verbose=True):
    lm = LayerMapping(LidarBorder, lidar_shape, lidar_mapping, transform=False)
    lm.save(strict=True, verbose=verbose)