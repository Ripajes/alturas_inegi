from rest_framework import viewsets
from rest_framework_gis import filters

from lidar.models import LidarBorder
from lidar.serializer import LidarSerializer

class LidarViewSet(viewsets.ReadOnlyModelViewSet):
    bbox_filter_field = "geom"
    filter_backends = (filters.InBBoxFilter,)
    queryset = LidarBorder.objects.all()
    serializer_class = LidarSerializer
