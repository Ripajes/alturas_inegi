from django.urls import path
from .views import LidarMapView, HomePageView, GeoJsonDetailView, model_form_upload, calcular_alturas, show_original_layer
from django.conf import settings
from django.conf.urls.static import static

app_name = "lidar"

urlpatterns = [
    path('geojson/<int:pk>/', GeoJsonDetailView.as_view(), name='geojson_detail'),
    path("loadShape/", model_form_upload, name='update_shape'),
    path("map/", LidarMapView.as_view(), name= 'map'),
    path('', HomePageView.as_view(), name='home' ),
    path('calcular_alturas/', calcular_alturas, name='calcular_alturas'),
    path('mostrar_original_layer/', show_original_layer, name='mostrar_layer'),
]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)