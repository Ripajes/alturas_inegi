# -*- coding: UTF-8 -*-
import os
from pathlib import Path
import json
import shutil
#from sqlalchemy import create_engine
import numpy as np
from osgeo import gdal, osr
from affine import Affine
from shapely.geometry import box
import geopandas as gpd
import rasterio as rio
from rasterio.mask import mask
from rasterio.features import shapes
from rasterio.windows import Window
from rasterio.transform import Affine
#from rasterio.plot import show
#from shapely.geometry import mapping
#import matplotlib.pyplot as plt


SRID_ITRF_ZONES={
    "2008": {
        "11":6366,
        "12":6367,
        "13":6368,
        "14":6369,
        "15":6370,
        "16":6371,        
    },
    "1992": {
        "11":4484,
        "12":4485,
        "13":4486,
        "14":4487,
        "15":4488,
        "16":4489,
    }
}

def get_raster_file(ruta):
    """
    Obtiene la ruta de los archivos raster para los tipos de archivo dentro de la lista rasterTypes
    
    Parameters:
    ruta (str): folder path where the rater is

    Returns:
    dict: raster with two keys (type and ruta) with extension and path of the raster file.
    """
    rasterTypes = ["xyz", "bil", "adf"]
    raster = None
    for folder, subfolder, files in os.walk(ruta):
        for file in files:
            fileType = file.split(".")[-1]
            if fileType in rasterTypes:
                raster = {}
                raster["type"] = fileType
                raster["ruta"] = os.path.join( folder, file)
                break
    return raster

def get_epsg_xyz(ruta_raster):
    """
    Obtiene la clave epsg de la proyección del archivo ruta_raster. Depende de que se tengan los archivos txt o html con información del raster.
    Esta función buscará éstos últimos archivos en la dicrección dos niveles arriba de la ubicación del raster.
    Sólo sirve para archivos ascii descargados de INEGI.

    Parametros:
    ruta_raster (dict): dictionario con dos claves (type y ruta) que contienen la ruta y el tipo del raster.
    
    Returns:
    int: clave de la proyección epsg
    """
    rasterinfo = {}
    folder = os.path.dirname(os.path.dirname(ruta_raster))

    fileTypes = ["xml"]
    for folder, subfolder, files in os.walk(folder):
        for file in files:
            fileType = file.split(".")[-1]
            if fileType in fileTypes:  
                rasterinfo[fileType] = os.path.join( folder, file)

    if "txt" in rasterinfo.keys():
        with open(rasterinfo["txt"], "r") as txtFile:
            for line in txtFile:
                if "ZONA_UTM" in line:
                    zona_utm = str(line.split(":")[1].strip())
                    print(zona_utm)
                if "DATUM_HORIZONTAL" in line:
                    if "92" in line:
                        itrf = "1992"
                    else:
                        itrf = "2008"
                #print(line)
    elif "xml" in rasterinfo.keys():
        import xml.etree.ElementTree as ET
        tree = ET.parse(rasterinfo["xml"])
        root = tree.getroot()
        zona_utm = root.find(".//utm_zone").text
        if "92" in root.find(".//utm_zone").text:
            itrf = "1992"
        else:
            itrf = "2008"

        
    epsg = SRID_ITRF_ZONES[itrf][zona_utm]
    print("epsg", epsg)
    return epsg

def check_raster(raster):
    """
    Convierte el archivo raster a un formato que se pueda utilizar y verifica si el cuenta con proyección

    Parameters:
    ruta_raster (dict): dictionario con dos claves (type y ruta) que contienen la ruta y el tipo del raster.

    Returns:
    dict: dictionario con dos claves (type y ruta) que contienen la ruta y el tipo del raster modificado en caso de que se haya modificado

    """
    print("check_raster", raster)
    new_raster = {}
    if raster["type"] == "xyz":
        new_raster["ruta"] = os.path.join(
            os.path.dirname(raster["ruta"]),
            os.path.basename(raster["ruta"]).split(".")[0] + ".tif"
        )
        new_raster["type"] = "tif"
        if not os.path.exists(new_raster["ruta"]):
            import numpy as np
            import pandas as pd
            import rasterio as rio
            from rasterio.transform import Affine

            dat = pd.read_table(raster["ruta"], sep=" ", header=None, dtype=float, low_memory=False)
            xmin = dat.iloc[:,0].min()
            xmax = dat.iloc[:,0].max()
            ymin = dat.iloc[:,1].min()
            ymax = dat.iloc[:,1].max()
            dx = dat.iloc[:,0].drop_duplicates().sort_values().diff().median()
            dy = dat.iloc[:,1].drop_duplicates().sort_values().diff().median()
            xv = pd.Series(np.arange(xmin, xmax + dx, dx))
            yv = pd.Series(np.arange(ymin, ymax + dy, dy)[::-1])
            xi = pd.Series(xv.index.values, index=xv)
            yi = pd.Series(yv.index.values, index=yv)
            nodata = np.nan
            zv = np.ones((len(yi), len(xi)), np.float32) * nodata
            zv[yi[dat[1]].values, xi[dat[0]].values] = dat[2]

            # register geotransform based on upper-left corner
            transform = Affine(dx, 0, xmin, 0, -dy, ymax) * Affine.translation(-0.5, -0.5)
            epsg = get_epsg_xyz(raster["ruta"])
            with rio.open(new_raster["ruta"], "w", "GTiff", len(xi), len(yi), 1, f"EPSG:{epsg}",
                            transform, rio.float32, nodata) as ds:
                ds.write(zv.astype(np.float32), 1)
        print(new_raster)
        return new_raster
    else:
        return raster

def raster_dif(raster_ter, raster_sup, raster_save):
    raster1 = rio.open(raster_ter["ruta"])
    no_data_raster1 = raster1.nodata
    print(no_data_raster1)
    #if no_data_raster1 == 0:
    #    raster1[raster1 == 0 ] = np.nan   #option 2
    
    raster2 = rio.open(raster_sup["ruta"])
    no_data_raster2 = raster1.nodata
    #if no_data_raster2 == 0:
    #    raster2[raster2 == 0 ] = np.nan   #option 2
    
    bb_raster1 = box(raster1.bounds[0], raster1.bounds[1], raster1.bounds[2], raster1.bounds[3])
    bb_raster2 = box(raster2.bounds[0], raster2.bounds[1], raster2.bounds[2], raster2.bounds[3])

    if bb_raster1 != bb_raster2:
        xminR1, yminR1, xmaxR1, ymaxR1 = raster1.bounds
        xminR2, yminR2, xmaxR2, ymaxR2 = raster2.bounds
        intersection = bb_raster1.intersection(bb_raster2)
        
        transform = Affine(raster1.res[0], 0.0, intersection.bounds[0], 0.0, -raster1.res[1], intersection.bounds[3])

        p1Y = intersection.bounds[3] - raster1.res[1]/2 # max_y -  height/2
        p1X = intersection.bounds[0] + raster1.res[0]/2 # min_x -  width/2
        p2Y = intersection.bounds[1] + raster1.res[1]/2 # min_y -  height/2
        p2X = intersection.bounds[2] - raster1.res[0]/2 # max_x -  width/2
        print("p1Y", "p1X", "p2Y", "p2X", p1Y, p1X, p2Y, p2X)
        #row index raster1
        row1R1 = int((ymaxR1 - p1Y)/raster1.res[1])
        #row index raster2
        row1R2 = int((ymaxR2 - p1Y)/raster2.res[1])
        #column index raster1
        col1R1 = int((p1X - xminR1)/raster1.res[0])
        #column index raster2
        col1R2 = int((p1X - xminR2)/raster1.res[0])
        print("row1R1 row1R2 col1R1 col1R2", row1R1, row1R2, col1R1, col1R2)
        #row index raster1
        row2R1 = int((ymaxR1 - p2Y)/raster1.res[1])
        #row index raster2
        row2R2 = int((ymaxR2 - p2Y)/raster2.res[1])
        #column index raster1
        col2R1 = int((p2X - xminR1)/raster1.res[0])
        #column index raster2
        col2R2 = int((p2X - xminR2)/raster1.res[0])

        width1 = col2R1 - col1R1 + 1
        width2 = col2R2 - col1R2 + 1
        height1 = row2R1 - row1R1 + 1
        height2 = row2R2 - row1R2 + 1
    
        arr_raster1 = raster1.read(1, window=Window(col1R1, row1R1, width1, height1), masked=True)
        
        arr_raster2 = raster2.read(1, window=Window(col1R2, row1R2, width2, height2), masked=True)
    else:
        transform = Affine(raster1.res[0], 0.0, raster1.bounds[0], 0.0, -raster1.res[1], raster1.bounds[3])
        arr_raster1 = raster1.read(1)
        arr_raster2 = raster2.read(1)
    
    if no_data_raster1 == 0:
        arr_raster1[arr_raster1 == 0 ] = np.nan
    if no_data_raster2 == 0:
        arr_raster2[arr_raster2 == 0 ] = np.nan
    
    arr_sum =  arr_raster2 - arr_raster1
    
    arr_sum[np.abs(arr_sum) > 1000  ] = np.nan   #option 2
    arr_sum = np.round(arr_sum, 1)
    
    with rio.open(raster_save, 
                       'w',
                       driver='GTiff',
                       height=arr_sum.shape[0],
                       width=arr_sum.shape[1],
                       count=1,
                       dtype=arr_sum.dtype,
                       crs=raster1.crs,
                       transform=transform) as dst:
        dst.write(arr_sum, 1)
    dst.close()
    return True

def obtener_alturas(cartas, DIRNAME):
    alturas_rasters = []
    for carta in cartas:
        carta_folder = os.path.join(DIRNAME, carta)
        raster_altura = os.path.join(carta_folder, f"{carta}_altura.tif")
        print(raster_altura, os.path.exists(raster_altura))
        if not os.path.exists(raster_altura):
            # calculamos el raster de altura
            raster_sup = get_raster_file(os.path.join(carta_folder, "superficie"))
            raster_ter = get_raster_file(os.path.join(carta_folder, "terreno"))
            raster_sup = check_raster(raster_sup)
            raster_ter = check_raster(raster_ter)
            raster_dif(raster_ter, raster_sup, raster_altura)
        alturas_rasters.append(raster_altura)
    return alturas_rasters

def get_alturas_array(id, pol_df, altura_rasters, figures_dir=False):
    clip_arrays = []
    for inras in altura_rasters:
        src  = rio.open(inras)
        pol_df = pol_df.to_crs(epsg=src.crs.to_epsg())
        #Parse features from GeoDataFrame in such a manner that rasterio wants them
        coords = [json.loads(pol_df.to_json())['features'][0]['geometry']]
        #
        try:
            clipped_array, clipped_transform = mask(dataset=src, shapes=coords, crop=True)
        except:
            clipped_array = None
        if clipped_array is not None:
            clipped_array[(clipped_array <= 0) ] = np.nan
            #if figures_dir:
            #    basenameRaster = os.path.basename(inras).split(".")[0]
            #    basenameRaster = basenameRaster.split("_")[0]
            #    out_tif = os.path.join(figures_dir, f"{id}_{basenameRaster}.tif")
            #    if not os.path.exists(out_tif):
            #        out_meta = src.meta.copy()
            #        out_meta.update({
            #            "driver": "GTiff",
            #            "height": clipped_array.shape[1],
            #            "width": clipped_array.shape[2],
            #            "transform": clipped_transform})
            #        with rio.open(out_tif, "w", **out_meta) as dest: dest.write(clipped_array)
                    #clipped = rasterio.open(out_tif)
                    #fig, ax = plt.subplots(figsize=(8, 6))
                    #p1 = df.plot(color=None,facecolor='none',edgecolor='red',linewidth = 2,ax=ax)
                    #show(clipped, ax=ax)
                    #ax.axis('off');
            clip_arrays.append(clipped_array)
    return clip_arrays

def get_alturas(arrays):
    print("Nuevo poligono")
    for idx_array, array in enumerate(arrays):
        array = array.flatten()
        print(array)
        if idx_array == 0:
            clipped_array = array
        else:
            clipped_array = np.concatenate((clipped_array, array))
    print(clipped_array)
    if not np.isnan(clipped_array).all():
        h_min = np.nanmin(clipped_array)
        h_max = np.nanmax(clipped_array)
        h_range = h_max - h_min
        h_mean = np.nanmean(clipped_array)
        h_std = np.nanstd(clipped_array,  ddof=1)    
    else:
        h_min, h_max, h_range, h_mean, h_std = np.nan, np.nan, np.nan, np.nan, np.nan
    return h_min, h_max, h_range, h_mean, h_std

def get_file_type_name(raster):
    filename = os.path.basename(raster["ruta"])
    extension = filename.split(".")[1]
    if extension == "adf":
        file_type_name = os.path.dirname(raster["ruta"])
        file_type_name = os.path.basename(file_type_name).split("_")[1]
    else:
        file_type_name = filename.split(".")[0].split("_")[1]
    return file_type_name

def verificar_descarga():
    DIRNAME = Path(r"C:\Users\Jesus R\Downloads\lidar_descarga")
    incorrectos = []
    desconocidos = []
    for folder in os.listdir(DIRNAME):
        folders = []
        sup_folder = Path(os.path.join(DIRNAME, folder, "superficie"))
        ter_folder = Path(os.path.join(DIRNAME, folder, "terreno"))
        print(Path(os.path.join(DIRNAME, folder)))
        
        if sup_folder.exists():
            sup_raster = get_raster_file(sup_folder)
            if sup_raster:
                print(sup_raster["ruta"])
                file_type_name = get_file_type_name(sup_raster)
                if file_type_name == 'mt':
                    #incorrectos.append(sup_raster["ruta"])
                    folders.append(sup_folder)
                else:
                    desconocidos.append(sup_raster["ruta"])

        if ter_folder.exists():
            ter_raster = get_raster_file(ter_folder)
            if ter_raster:
                print(ter_raster["ruta"])
                file_type_name = get_file_type_name(ter_raster)
                if file_type_name == 'ms':
                    #incorrectos.append(ter_raster["ruta"])
                    folders.append(ter_folder)
                else:
                    desconocidos.append(ter_raster["ruta"])
        if len(folders) >0:
            incorrectos.append({folder: folders})
    return incorrectos, desconocidos