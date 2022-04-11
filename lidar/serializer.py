from rest_framework_gis import fields, serializers
from lidar.models import LidarBorder

class LidarSerializer(serializers.GeoFeatureModelSerializer):
    class Meta:
        fields = ("id", "clave10k")
        geo_field = "geom"
        model = LidarBorder