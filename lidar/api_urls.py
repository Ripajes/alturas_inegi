from rest_framework import routers
from lidar.api_views import LidarViewSet

router = routers.DefaultRouter()
router.register(r"lidar", LidarViewSet)

urlpatterns = router.urls