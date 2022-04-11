from django.db.models import fields
from django_tables2 import tables
from .models import Poligonos

class PoligonoTable(tables.Table):
    class Meta:
        model = Poligonos
        fields = ('id','h_min', 'h_max', 'h_range', 'h_mean','h_std')
        order_by = 'id'  # use dash for descending order
        orderable=True
        template_name = "django_tables2/bootstrap.html"