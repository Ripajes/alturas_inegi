#from django.views.generic.base import TemplateView
from logging import setLoggerClass
from typing import ItemsView
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView, DetailView, ListView
from django.http import JsonResponse

from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django_tables2.data import TableQuerysetData
from .forms import DocumentForm
from .models import Document, Poligonos
from .tables import PoligonoTable
from django_tables2 import RequestConfig

from utils.read_geojson import geojson_aturas
from utils.Layers import get_original_layer
from utils.read_geojson import procesar_shapefile
import json
from django.shortcuts import get_object_or_404
import os

# Create your views here.
class HomePageView(ListView):
    model = Document
    template_name = 'home.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Document.objects.filter(author=self.request.user)

class LidarMapView(TemplateView):
    template_name = "map.html"
    context_object_name = 'lidar_map'

class GeoJsonDetailView(DetailView):
    model= Document
    table_class = PoligonoTable
    template_name='geojson_detail.html'
    table_pagination = {
        'per_page': 10
    }
    #def get_queryset(self):
    #    self.document = get_object_or_404(Document, id=self.kwargs['id'])
    #    return Poligonos.objects.filter(fileid=self.document)

    def get_context_data(self, **kwargs):
        context = super(GeoJsonDetailView, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        table = self.table_class(Poligonos.objects.filter(fileid=self.get_object().pk))
        table.paginate(per_page=20)
        #RequestConfig(self.request, paginate=self.get_table_pagination(table)).configure(table)
        context['table'] = table
        #print(context['poligonos'])
        return context

def model_form_upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        #spatial_file = form['document'].value()
        #if spatial_file.endswith(".shp"):
        #    shape_path = spatial_file
        #    column_id = form['original_id'].value()
        #    document_id = form['my_field'].value()
        #    procesar_shapefile(shape_path, column_id, document_id)

        if form.is_valid():
            form.save()
            return redirect('lidar:home')
    else:
        form = DocumentForm()
    return render(request, 'load_shape.html', {'form': form})

def calcular_alturas(request):
    if request.method == 'GET' and request.is_ajax():
        # do something
        documentid = request.GET.get('documentid')
        geojson_alturas = geojson_aturas(Document.objects.get(id=documentid))
        response_data = {
            "rawData": geojson_alturas
        }
        # return response
        return JsonResponse(response_data, status=200)

def show_original_layer(request):
    if request.method == 'GET' and request.is_ajax():
        # do something
        documentid = request.GET.get('documentid')
        geojson_alturas = get_original_layer(Document.objects.get(id=documentid))
        response_data = {
            "rawData": geojson_alturas
        }
        # return response
        return JsonResponse(response_data, status=200)