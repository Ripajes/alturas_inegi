# -*- coding: UTF-8 -*-
from django import shortcuts
from django.conf import settings
from django.db import connection
from django.contrib.gis.geos import GEOSGeometry
from lidar.models import Poligonos
import geopandas as gpd
import os
from .descargarLidar import get_urls, descargar
from .lidarProcesamiento import obtener_alturas, get_alturas, get_alturas_array
import os
import numpy as np

MEDIA_ROOT = settings.MEDIA_ROOT

def display_text_file(self):
        with open(self.document.path) as fp:
            return fp.read()

def geojson_aturas(geojson_obj):
    pathFile = geojson_obj.document.path
    #print(pathFile)
    cartas = gpd.GeoDataFrame.from_postgis("""SELECT * FROM "lidar_lidarborder" order by id""", con=connection)
    polygons = gpd.GeoDataFrame.from_postgis(f"""SELECT * FROM "lidar_poligonos" WHERE fileid_id = {geojson_obj.id} order by id""", con=connection)

    if not polygons.shape[0] > 0:
        polygons = gpd.read_file(pathFile)
        polygons = polygons.to_crs(4326)
        polygons = polygons.loc[:, [geojson_obj.original_id, "geometry"]]

        intersections= gpd.sjoin(polygons, cartas, how="left", op='intersects')

        cartas_lista = intersections["clave10k"].unique()

        folder_descarga = os.path.join(MEDIA_ROOT, "rasters")
        if not os.path.exists(folder_descarga):
            os.mkdir(folder_descarga)
        folder_imagenes = os.path.join(MEDIA_ROOT, "imgs")
        if not os.path.exists(folder_imagenes):
            os.mkdir(folder_imagenes)
        
        tipos = ["Superficie", "Terreno"]
        cartas_verificadas = []

        for clave_carta in cartas_lista:
            #print(clave_carta)
            urls = get_urls(clave_carta, tipos)
            #print(urls)
            if len(urls["Superficie"]) > 0 and len(urls["Terreno"]) > 0:
                carta_folder = os.path.join(folder_descarga, clave_carta)
                raster_altura = os.path.join(carta_folder, f"{clave_carta}_altura.tif")
                if not os.path.exists(raster_altura):
                    descargar(folder_descarga, clave_carta, urls, tipos)
                cartas_verificadas.append(clave_carta) 

        alturas_rasters = obtener_alturas(cartas_verificadas, folder_descarga)
        polygons["fileid_id"]=geojson_obj.id
        polygons["h_min"]=np.nan
        polygons["h_max"]=np.nan
        polygons["h_range"]=np.nan
        polygons["h_mean"]=np.nan
        polygons["h_std"]=np.nan

        for index, pol in polygons.iterrows():
            #print(index)
            id_pol = pol[geojson_obj.original_id]
            pol_df = polygons.loc[polygons[geojson_obj.original_id] == id_pol]
            lidar_extension = intersections[intersections[geojson_obj.original_id] == id_pol]
            cartas = []
            for i_lidar, lidar_ in lidar_extension.iterrows():
                if lidar_["clave10k"] in cartas_verificadas:
                    cartas.append(lidar_["clave10k"])
            if len(cartas)  > 0:
                #print(index, cartas)
                clip_arrays = get_alturas_array(id_pol,pol_df, alturas_rasters, folder_imagenes)
                h_min, h_max, h_range, h_mean, h_std = get_alturas(clip_arrays)
                polygons.loc[index, ["h_min", "h_max", "h_range", "h_mean", "h_std"]] = h_min, h_max, h_range, h_mean, h_std
                #print(polygons.loc[index])
        #polygons = polygons.loc[:, ["id_", "geometry", "h_min", "h_max", "h_range", "h_mean", "h_std"]]
        #polygons = polygons.to_crs(4326)
        polygons['geom'] = polygons.geometry.to_wkt()

        polygons.rename(columns={geojson_obj.original_id: "original_id"}, errors="raise", inplace=True)

        polygons['geom'] = polygons.geometry.to_wkt()
        pols_2 = polygons.drop('geometry', 1)

        #polygons.to_postgis("lidar_poligonos", con=connection, if_exists='append')
        for data in pols_2.to_dict("records"):
            geometry_str = data.pop('geom')
            geometry = GEOSGeometry(geometry_str)
            #try:
                
            #except (TypeError, ValueError) as exc:
                # If the geometry_str is not a valid WKT, EWKT or HEXEWKB string
                # or is None then either continue, break or do something else.
                # I will go with continue here.
            #    continue
            Poligonos.objects.update_or_create(
                geom=geometry,
                defaults=data
            )
    return polygons.to_json(na='null')

def procesar_shapefile(shape_path, column_id, document_id):
    shapefile = gpd.read_file(shape_path)
    shapefile = shapefile.to_crs(4326)
    shapefile = shapefile.loc[:, [column_id, "geometry"]]
    cartas = gpd.GeoDataFrame.from_postgis("""SELECT * FROM "lidar_lidarborder" order by id""", con=connection)

    intersections= gpd.sjoin(shapefile, cartas, how="left", op='intersects')
    cartas_lista = intersections["clave10k"].unique()
    folder_descarga = os.path.join(MEDIA_ROOT, "rasters")
    if not os.path.exists(folder_descarga):
        os.mkdir(folder_descarga)
    folder_imagenes = os.path.join(MEDIA_ROOT, "imgs")
    if not os.path.exists(folder_imagenes):
        os.mkdir(folder_imagenes)
    
    tipos = ["Superficie", "Terreno"]
    cartas_verificadas = []

    for clave_carta in cartas_lista:
        #print(clave_carta)
        urls = get_urls(clave_carta, tipos)
        #print(urls)
        if len(urls["Superficie"]) > 0 and len(urls["Terreno"]) > 0:
            carta_folder = os.path.join(folder_descarga, clave_carta)
            raster_altura = os.path.join(carta_folder, f"{clave_carta}_altura.tif")
            if not os.path.exists(raster_altura):
                descargar(folder_descarga, clave_carta, urls, tipos)
            cartas_verificadas.append(clave_carta) 

    alturas_rasters = obtener_alturas(cartas_verificadas, folder_descarga)
    shapefile["fileid_id"]=document_id
    shapefile["h_min"]=np.nan
    shapefile["h_max"]=np.nan
    shapefile["h_range"]=np.nan
    shapefile["h_mean"]=np.nan
    shapefile["h_std"]=np.nan

    for index, pol in shapefile.iterrows():
        id_pol = pol["id_"]
        pol_df = shapefile.loc[shapefile["id_"] == id_pol]
        lidar_extension = intersections[intersections["id_"] == id_pol]
        cartas = []
        for i_lidar, lidar_ in lidar_extension.iterrows():
            if lidar_["clave10k"] in cartas_verificadas:
                cartas.append(lidar_["clave10k"])
        if len(cartas)  > 0:
            clip_arrays = get_alturas_array(id_pol,pol_df, alturas_rasters, folder_imagenes)
            h_min, h_max, h_range, h_mean, h_std = get_alturas(clip_arrays)
            shapefile.loc[index, ["h_min", "h_max", "h_range", "h_mean", "h_std"]] = h_min, h_max, h_range, h_mean, h_std

    shapefile['geom'] = shapefile.geometry.to_wkt()
    shapefile.rename(columns={column_id: "original_id"}, errors="raise", inplace=True)
    shapefile['geom'] = shapefile.geometry.to_wkt()
    pols_2 = shapefile.drop('geometry', 1)
    print(pols_2.head(1))
    for data in pols_2.to_dict("records"):
        geometry_str = data.pop('geom')
        geometry = GEOSGeometry(geometry_str)
        Poligonos.objects.update_or_create(
            geom=geometry,
            defaults=data
        )