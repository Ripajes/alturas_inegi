from django.contrib.gis.db import models
from django.db.models.base import ModelState
from django.urls import reverse

# Create your models here.
class LidarBorder(models.Model):
    clave10k = models.CharField(max_length=8)
    geom= models.MultiPolygonField(srid=4326)

class Document(models.Model):
    title = models.CharField(max_length=200, default='')
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE
    )
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/%Y/%m/%d/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    original_id = models.CharField(max_length=50, default='id_')
    #file_path = models.CharField(max_length=255, default='')

    def __str__(self):
        return self.description

    def get_absolute_url(self):
        return reverse('geojson_detail', args=[str(self.id)])

class Poligonos(models.Model):
    fileid = models.ForeignKey(Document, on_delete=models.CASCADE)
    original_id = models.BigIntegerField()
    geom = models.MultiPolygonField(srid=4326, null=True)
    h_min = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    h_max = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    h_range = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    h_mean = models.DecimalField(max_digits=7, decimal_places=2, null=True)
    h_std = models.DecimalField(max_digits=7, decimal_places=2, null=True)