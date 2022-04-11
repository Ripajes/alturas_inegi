# -*- coding: UTF-8 -*-

import requests, zipfile
from io import BytesIO
import os
import time

import requests
import json
import time
import math
from requests.sessions import session
#from sqlalchemy import create_engine
#
from .inegiApi import get_raster_total, get_raster_list, get_mapa_info, grad_to_dec, get_epsg, get_utm_zone
#from dataBase import procesar_datos_inegi
import geopandas as gpd
    
def check_folder(ruta):
    if not os.path.exists(ruta):
        os.mkdir(ruta)

#def descargar(folder_descarga, clave_carta, urls, tipos, id, engine):
def descargar(folder_descarga, clave_carta, urls, tipos):
    #
    folder_carta = os.path.join(folder_descarga,clave_carta)
    check_folder(folder_carta)
    superficie_folder = os.path.join(folder_carta, "superficie")
    check_folder(superficie_folder)
    terreno_folder = os.path.join(folder_carta, "terreno")
    check_folder(superficie_folder)
    # descargamos el de superficie:
    sup_urls = urls["Superficie"]
    ter_urls = urls["Terreno"]
    #unk_urls = urls[""]
    #print("Revisando")
    urls = []
    sup_url= None
    ter_url = None
    if len(sup_urls.keys()) > 0:
        if 'bil' in sup_urls.keys():
            sup_url = sup_urls["bil"]
        elif 'ascii' in sup_urls.keys():
            sup_url = sup_urls["ascii"]
        elif 'grid'in sup_urls.keys():
            sup_url = sup_urls["grid"]
        if sup_url:
            urls.append({"tipo": "Superficie", "url": sup_url})
            #strSQL = f""" UPDATE lidar."cartas_10k" SET sup = True WHERE id = {id} """
            #with engine.connect() as connection: connection.execute(strSQL)
    else:
        pass
        #strSQL = f""" UPDATE lidar."cartas_10k" SET sup = False WHERE id = {id} """
        #with engine.connect() as connection: connection.execute(strSQL)
            
    if len(ter_urls.keys()) > 0:
        if 'ascii' in ter_urls.keys():
            ter_url = ter_urls["ascii"]
        elif 'bil' in ter_urls.keys():
            ter_url = ter_urls["bil"]
        elif 'grid'in ter_urls.keys():
            ter_url = ter_urls["grid"]
        if ter_url:
            urls.append({"tipo": "Terreno", "url": ter_url})
            #strSQL = f""" UPDATE lidar."cartas_10k" SET ter = True WHERE id = {id} """
            #with engine.connect() as connection: connection.execute(strSQL)
    else:
        pass
        #strSQL = f""" UPDATE lidar."cartas_10k" SET ter = False WHERE id = {id} """
        #with engine.connect() as connection: connection.execute(strSQL)
                  
    for url_ in urls:
        url = url_["url"]
        tipo = url_["tipo"]       
        #
        extracted_folder = url.split("/")[-1].split(".")[0]
        if tipo in tipos:
            if tipo == "Superficie":
                extracted_folder = os.path.join(superficie_folder, url.split("/")[-1].split(".")[0])
            elif tipo == "Terreno":
                extracted_folder = os.path.join(terreno_folder, url.split("/")[-1].split(".")[0])

        if not os.path.exists(extracted_folder):
            seguir = False
            time_sleep = [1,2,4,8,15,32,64]
            i = 0
            while seguir == False:
                try:
                    with requests.session() as client:
                        client.get('https://www.inegi.org.mx')
                        header_info = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
                            "Accept-Encoding": "*",
                            "Connection": "keep-alive"}
                        request = requests.get(url, headers=header_info)
                        time.sleep(1/10)
                        with zipfile.ZipFile(BytesIO(request.content)) as z:
                            z.extractall(extracted_folder)
                    seguir = True
                except:
                    if i < len(time_sleep):
                        time.sleep(time_sleep[i])
                        i += 1
                    else:
                        i=0
                        time.sleep(time_sleep[i])
                    seguir =False
                    print("Intentando descargar el zip")

def get_urls(clave_carta, tipos):
    urls = {"Superficie":{}, "Terreno": {}, "":{}}
    #print("get_urls", clave_carta)
    lista_rasters = get_raster_list(clave_carta=clave_carta)
    #print("get_lista_rasters")
    if lista_rasters:
        mapas = lista_rasters["mapas"]
        for mapa in mapas:
            tipo = ""
            formatos = mapa["formatos"]
            #print(mapa["titulo"].lower())
            try: tipo = mapa["titulo"].split(".")[-3].strip()
            except: pass
            for formato in formatos:
                url = formato["url"]["valor"]
                archivo = {}
                if tipo not in tipos:
                    try: tipo = url.split("/")[-2].split("_")[0]
                    except: pass
                    if tipo not in tipos:
                        if "terreno" in mapa["titulo"].lower():
                            tipo = "Terreno"
                        elif "superficie" in mapa["titulo"].lower():
                            tipo = "Superficie"
                url = "https://www.inegi.org.mx" + url
                urls[tipo][formato["extension"]] = url
        return urls
    else:
        return False

def main():
    engine = create_engine('postgresql+psycopg2://postgres:Dutu7029@localhost/maria')
    cartas = gpd.GeoDataFrame.from_postgis("""SELECT * FROM lidar."cartas_10k" where lidar is null order by id""", con=engine)
    # 
    total = cartas[cartas.columns[0]].count()
    folder_descarga = r"C:\Users\Jesus R\Downloads\lidar_descarga"
    tipos = ["Superficie", "Terreno"]


    for index, row in cartas.iterrows():
        clave_carta = row["clave10k"]
        lidar = row["lidar"]
        if lidar not in [False, True]:
            urls = get_urls(clave_carta, tipos)
            if urls:        
                descargar(folder_descarga, clave_carta, urls, tipos, row["id"], engine)
                strSQL = f"""UPDATE lidar."cartas_10k" SET lidar = True WHERE id = {row["id"]}"""
                with engine.connect() as connection:
                    connection.execute(strSQL)
                print(index, total, clave_carta ,"  tiene lidar")
            else:
                strSQL = f"""UPDATE lidar."cartas_10k" SET lidar = False WHERE id = {row["id"]}"""
                with engine.connect() as connection:
                    connection.execute(strSQL)
                print(index, total, clave_carta ," no tiene lidar")
            #break
        else: print(index, total, clave_carta , " ya se procesó")


if __name__ == '__main__':
    main()