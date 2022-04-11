# -*- coding: UTF-8 -*-
import requests
import json
import time
import math

def post_request(url, data):
    headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
    }
    #with requests.session() as client:
        #client.get('https://www.inegi.org.mx')
    header_info = {
        "POST": "/app/api/productos/interna_v2/componente/mapas/lista/resultados HTTP/1.1",
        "Host": "www.inegi.org.mx",
        "Connection": "keep-alive",
        "Content-Length": "249",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36",
        "Origin": "https://www.inegi.org.mx",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.inegi.org.mx/temas/relieve/continental/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "es-ES,es;q=0.9",
        "sec-ch-ua": '"Google Chrome";v="95", "Chromium";v="95", ";Not A Brand";v="99"',
        "sec-ch-ua-platform": '"Windows"'
    }
    r = requests.post(url,json=data)
    #data1 = json.loads(r.text)
    return json.loads(r.text)
    """print(data1.keys())
    continuar = False
    while continuar == False:
        try:
            #r = client.post(url, json=data, headers = header_info)
            r = requests.post(url,json=data, headers=header_info)
            time.sleep(1/10)
            continuar=True
            print(r.status_code)
            if r.status_code == 200:
                continuar=False
                return json.loads(r.text)
            else:
                return False
        except:
            print("Reintentando en 5 segundos")
            time.sleep(1)"""
                
        

def get_raster_estados():
    url = "https://www.inegi.org.mx/app/api/productos/interna_v2/componente/mapas/combos?opt=2"
    data = {
        "enti":"",
        "muni":"",
        "loca":"",
        "tema":"193",
        "titg":"",
        "esca":"",
        "edic":"",
        "form":"",
        "seri":"",
        "clave":"",
        "rango":"",
        "busc":"",
        "tipoB":2,
        "adv":False,
        "wordag":False,
        "mkeys":"",
        "mageo":"",
        "formIncl":None,
        "formExcl":None
    }
    response_ = post_request(url, data)
    if response_:
        return response_["list"]
    else:
        print("Error")
        return False

def get_raster_escala():
    url = "https://www.inegi.org.mx/app/api/productos/interna_v2/componente/mapas/combos?opt=4"
    headers = {
        "POST": "/app/api/productos/interna_v2/componente/mapas/lista/resultados HTTP/1.1",
        "Host": "www.inegi.org.mx",
        "Connection": "keep-alive",
        "Content-Length": "241",
        "sec-ch-ua": '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "sec-ch-ua-platform": '"Windows"',
        "Origin": "https://www.inegi.org.mx",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.inegi.org.mx/temas/relieve/continental/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "es-ES,es;q=0.9",
        "Cookie": "NSC_MC_OvfwpQpsubm=ffffffff09911c5945525d5f4f58455e445a4a423660; _ga=GA1.3.1034875415.1634848350; _gid=GA1.3.1257346116.1634848350; NSC_MC_dpoufojept2=ffffffff09da7a5445525d5f4f58455e445a4a4229a2; NSC_MC_bqjt=ffffffff09911cc745525d5f4f58455e445a4a423660; _gat=1"
    }
    data = {
        "enti":"",
        "muni":"",
        "loca":"",
        "tema":"193",
        "titg":"",
        "esca":"",
        "edic":"",
        "form":"",
        "seri":"",
        "clave":"",
        "rango":"",
        "busc":"",
        "tipoB":2,
        "adv":False,
        "wordag":False,
        "mkeys":"",
        "mageo":"",
        "formIncl":None,
        "formExcl":None
    }
    response_ = post_request(url, data)
    if response_: return response_["list"]
    else:
        print("Error")
        return False

def get_raster_año():
    url = "https://www.inegi.org.mx/app/api/productos/interna_v2/componente/mapas/combos?opt=5"
    headers = {
        "POST": "/app/api/productos/interna_v2/componente/mapas/lista/resultados HTTP/1.1",
        "Host": "www.inegi.org.mx",
        "Connection": "keep-alive",
        "Content-Length": "241",
        "sec-ch-ua": '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "sec-ch-ua-platform": '"Windows"',
        "Origin": "https://www.inegi.org.mx",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.inegi.org.mx/temas/relieve/continental/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "es-ES,es;q=0.9",
        "Cookie": "NSC_MC_OvfwpQpsubm=ffffffff09911c5945525d5f4f58455e445a4a423660; _ga=GA1.3.1034875415.1634848350; _gid=GA1.3.1257346116.1634848350; NSC_MC_dpoufojept2=ffffffff09da7a5445525d5f4f58455e445a4a4229a2; NSC_MC_bqjt=ffffffff09911cc745525d5f4f58455e445a4a423660; _gat=1"
    }
    data = {
        "enti":"",
        "muni":"",
        "loca":"",
        "tema":"193",
        "titg":"",
        "esca":"",
        "edic":"",
        "form":"",
        "seri":"",
        "clave":"",
        "rango":"",
        "busc":"",
        "tipoB":2,
        "adv":False,
        "wordag":False,
        "mkeys":"",
        "mageo":"",
        "formIncl":None,
        "formExcl":None
    }
    response_ = post_request(url, data)
    if response_: return response_["list"]
    else:
        print("Error")
        return False

def get_raster_total():
    url = "https://www.inegi.org.mx/app/api/productos/interna_v2/componente/mapas/total"
    headers = {
        "POST": "/app/api/productos/interna_v2/componente/mapas/total HTTP/1.1",
        "Host": "www.inegi.org.mx",
        "Connection": "keep-alive",
        "Content-Length": "217",
        "sec-ch-ua": '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "sec-ch-ua-platform": '"Windows"',
        "Origin": "https://www.inegi.org.mx",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.inegi.org.mx/temas/relieve/continental/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "es-ES,es;q=0.9",
        "Cookie": "_ga=GA1.3.1886868478.1583429508; ai_user=bvkLWvNyQbeUtyjJRQC3DQ|2021-09-23T18:27:54.781Z; _gid=GA1.3.624642788.1634741954; NSC_MC_OvfwpQpsubm=ffffffff09da7a3e45525d5f4f58455e445a4a423660; _gat=1; NSC_MC_bqjt=ffffffff09911cc745525d5f4f58455e445a4a423660",
    }
    data = {
        "enti":"",
        "muni":"",
        "loca":"",
        "tema":"193",
        "titg":"",
        "esca":8,
        "edic":"",
        "form":"",
        "seri":"",
        "clave":"",
        "rango":"",
        "busc":"",
        "tipoB":2,
        "adv":False,
        "wordag":False,
        "mkeys":"",
        "mageo":"",
        "formIncl":None,
        "formExcl":None
    }
    response_ = post_request(url, data)
    if response_: return response_
    else: return False

def get_raster_list(pag=0, clave_carta=""):
    print("Obteniendo raster List")
    headers = {
        "POST": "/app/api/productos/interna_v2/componente/mapas/lista/resultados HTTP/1.1",
        "Host": "www.inegi.org.mx",
        "Connection": "close",
        "Content-Length": "241",
        "sec-ch-ua": '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "sec-ch-ua-platform": '"Windows"',
        "Origin": "https://www.inegi.org.mx",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.inegi.org.mx/temas/relieve/continental/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "es-ES,es;q=0.9",
        "Cookie": "NSC_MC_OvfwpQpsubm=ffffffff09911c5945525d5f4f58455e445a4a423660; _ga=GA1.3.1034875415.1634848350; _gid=GA1.3.1257346116.1634848350; NSC_MC_dpoufojept2=ffffffff09da7a5445525d5f4f58455e445a4a4229a2; NSC_MC_bqjt=ffffffff09911cc745525d5f4f58455e445a4a423660; _gat=1"
    }
    url = "https://www.inegi.org.mx/app/api/productos/interna_v2/componente/mapas/lista/resultados"
    data = {"enti":"",
            "muni":"",
            "loca":"",
            "tema":"193",
            "titg":"",
            "esca":8,
            "edic":"",
            "form":"",
            "seri":"",
            "clave":"",
            "rango":"",
            "busc":clave_carta,
            "tipoB":2,
            "adv":False,
            "mkeys":"",
            "mageo":"",
            "formIncl":None,
            "formExcl":None,
            "orden":4,
            "desc":True,
            "pag":pag,
            "tam":100
           }
    seguir = False
    while seguir == False:
        response_ = post_request(url, data)
        #print(response_)
        if response_:
            if response_["success"] == True:
                return response_['list']
            else:
                print(response_)
                if "message" in response_.keys():
                    if response_["message"] == "No existe información para el listado de cartas":
                        return False
                
        else:
            #print(response_)
            print("Intentando hacer de nuevo la petición a la API de Inegi")
            time.sleep(4)

    


def get_mapa_info(upc):
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "es-ES,es;q=0.9",
        'Connection':'close',
        "Cookie": "_ga=GA1.3.1886868478.1583429508; ai_user=bvkLWvNyQbeUtyjJRQC3DQ|2021-09-23T18:27:54.781Z; _gid=GA1.3.624642788.1634741954; NSC_MC_OvfwpQpsubm=ffffffff09da7a3e45525d5f4f58455e445a4a423660; NSC_MC_bqjt=ffffffff09911cc745525d5f4f58455e445a4a423660; _gat=1; NSC_MC_dpoufojept2=ffffffff09da7a5445525d5f4f58455e445a4a4229a2",
        "Host": "www.inegi.org.mx",
        "Referer": "https://www.inegi.org.mx/app/biblioteca/ficha.html?upc=889463839545",
        "sec-ch-ua": '"Chromium";v="94", "Google Chrome";v="94", ";Not A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
    }
    url = f"https://www.inegi.org.mx/app/api/productos/interna_v2/ficha/datos?upc={upc}&lang=false"
    r = requests.get(url)
    time.sleep(1/10)
    if r.status_code == 200:
        json_data = json.loads(r.text)
        return json_data['info']['generales']
    else: return False

def grad_to_dec(grad):
    grados, minutos, segundos = grad.split(" ")
    grados = int(grados[:-1])
    minutos = int(minutos)
    segundos = float(segundos[:-1])
    return grados + minutos/60 + segundos/3600

def get_epsg(utm_zone, datum):
    epsgs = {
        "ITRF92":{
            11: 4484,
            12: 4485,
            13: 4486,
            14: 4487,
            15: 4488,
            16: 4489
        },
        "ITRF08":{
            11: 6366,
            12: 6367,
            13: 6368,
            14: 6369,
            15: 6370,
            16: 6371,
        }            
    }
    return epsgs[datum][utm_zone]

def get_utm_zone(coord):
    zone = 30
    for x in range(0,180, 6):
        if coord >= x and coord <= x+6:
            return zone
        else:
            zone -= 1

if __name__ == '__main__':
    estados = get_raster_estados()