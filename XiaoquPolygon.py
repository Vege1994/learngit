# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 16:23:20 2020

@author: 11717
"""
import requests
import math
from urllib.parse import urlencode
import pandas as pd
from tqdm import tqdm
import time


def GCJ2WGS(location):
    # 将高德GCJ坐标转为GPS坐标
    # location格式如下：locations[1] = "113.923745,22.530824"
    if isinstance(location, str):
        lon = float(location[0:location.find(",")])
        lat = float(location[location.find(",") + 1:len(location)])
    else:
        lon = location[0]
        lat = location[1]
    a = 6378245.0 # 克拉索夫斯基椭球参数长半轴a
    ee = 0.00669342162296594323 #克拉索夫斯基椭球参数第一偏心率平方
    PI = 3.14159265358979324 # 圆周率
    # 以下为转换公式
    x = lon - 105.0
    y = lat - 35.0
    # 经度
    dLon = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x));
    dLon += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0;
    dLon += (20.0 * math.sin(x * PI) + 40.0 * math.sin(x / 3.0 * PI)) * 2.0 / 3.0;
    dLon += (150.0 * math.sin(x / 12.0 * PI) + 300.0 * math.sin(x / 30.0 * PI)) * 2.0 / 3.0;
    #纬度
    dLat = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x));
    dLat += (20.0 * math.sin(6.0 * x * PI) + 20.0 * math.sin(2.0 * x * PI)) * 2.0 / 3.0;
    dLat += (20.0 * math.sin(y * PI) + 40.0 * math.sin(y / 3.0 * PI)) * 2.0 / 3.0;
    dLat += (160.0 * math.sin(y / 12.0 * PI) + 320 * math.sin(y * PI / 30.0)) * 2.0 / 3.0;
    radLat = lat / 180.0 * PI
    magic = math.sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = math.sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * PI);
    dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * PI);
    wgsLon = lon - dLon
    wgsLat = lat - dLat
    return wgsLon,wgsLat

keys = ['6aa89a380342ab9b5beedb6bb3ea42aa', '3a14d4c5ee16e5b8da03f4431a91072a'
        , '7ab712462cb8fe0eaf6c8ecfbd0376e7', '7041f4c051b5189e81f651f06a7883bd'
        , '40652da1f9b4af3af38e14b7cc48c230', '67fc565d6348d4c8e184d82afa34ef09'
        , '3fd486fa32362598ecd5406a592c2747', '	84482d1e5b6b28d5baf4179b0bc43adb'
        , '6a54cbcccbbbc42e05e82feab9f5aec8', 'd3be9afa9258fd16d40c8b57ef8e62f7'
        ]

currkey = 3

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"
        , "cookie": "cna=DKmEFj+SFnACAT2Mty7POMrj; passport_login=MzAzMTg5ODAyLGFtYXBfMTg5MjQ5NTIyODdCeFh2RWRDdXQsemZ2aWZ5M3RwcWM0cmhwY2kydW16dmhodW5wZGRreXYsMTU4MDczOTUzNCxNMkV4WW1NeVl6SmtZamsxT0RBME5qazJaR05oWW1Wa1lqQTVZVEppT1dVPQ%3D%3D; dev_help=1%2B%2FChIuAAence7QrEhYE8zcwZjk1NzRjNGZjYWZhNzIyNzI5ZGU1MjMwNDIyNzJlODk5MzNjOWY5YmQ5NGRlNDJlZGQyYzE2MWM1ZDc1YzMmQnaU88%2BTdYJAiZ9ckdQmWJ2hW6FEsEksZY7zH4OHo0fXKOVUPpdhPmbaP6qC0uQ74WCKGDfY%2FJRqrqS5fTgw2gR808OGjDmmMMVS7%2BhlOGhFINM0OrDRp7nmHyKP3DBQ9TpiLoe4Sw5IlrxV0b43; l=cBrqA3erQMai2oSzKOCanurza77OSIRYYuPzaNbMi_5Qq6T1XPBOo2AYyF96VjWd9DTB46VFKQp9-etuZ8c3xfBR2ZPc.; isg=BHV1IZcWRwucr6OwTIytbWE0hPEv8ikEAWdx6_eaNew7zpXAv0Dr1FXMHJJ4iUG8; x5sec=7b22617365727665723b32223a223263333263306335616432376664343938393132376133643063396366666433434d4831672f49464550543437763378784f69446941453d227d"
        }

headers2 = {}
#headers2["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
#headers2["Cookie"] = "cna=DKmEFj+SFnACAT2Mty7POMrj; passport_login=MzAzMTg5ODAyLGFtYXBfMTg5MjQ5NTIyODdCeFh2RWRDdXQsemZ2aWZ5M3RwcWM0cmhwY2kydW16dmhodW5wZGRreXYsMTU4MDczOTUzNCxNMkV4WW1NeVl6SmtZamsxT0RBME5qazJaR05oWW1Wa1lqQTVZVEppT1dVPQ%3D%3D; dev_help=1%2B%2FChIuAAence7QrEhYE8zcwZjk1NzRjNGZjYWZhNzIyNzI5ZGU1MjMwNDIyNzJlODk5MzNjOWY5YmQ5NGRlNDJlZGQyYzE2MWM1ZDc1YzMmQnaU88%2BTdYJAiZ9ckdQmWJ2hW6FEsEksZY7zH4OHo0fXKOVUPpdhPmbaP6qC0uQ74WCKGDfY%2FJRqrqS5fTgw2gR808OGjDmmMMVS7%2BhlOGhFINM0OrDRp7nmHyKP3DBQ9TpiLoe4Sw5IlrxV0b43; l=cBrqA3erQMai2v12BO5aourza77tniAfVyy0aNbMiIEPC6xhQypQpmxQLvvHlB-RR8XFTPy9qy1H39qM-9U38yXfpUg5dm2ASj5..; isg=BKKiDhmlCLzabxQZN23y9Dpl8ygE86YNqjbmguwLxp9Ev8s5cYOXHLH97_tDqR6l"
#headers2["Host"] = "restapi.amap.com"
headers2["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.87 Safari/537.36"
#headers2["Cache-Control"] = "max-age=0"
#headers2["Pragma"] = "no-cache"

def geocode(add):
    """
    :param add:{'city':str, 'address': str}
    :return:
    """
    # add = ''.join(['浙江省', '宁波市', '余姚市'] + address)
    global currkey
    url = 'https://restapi.amap.com/v3/geocode/geo?key={2}&address={0}&output=json&city={1}'.format(add['address'], add['city'], keys[currkey])
    print(add, '\n', url)
    rawdata = requests.get(url, headers=headers)
    data = rawdata.json()
#    print(data)
    if data["infocode"] != "10000":
        print(data)
    if data["count"] == "0":
        return None
    # print(data)
#    return data['geocodes'][0]['location']
#    return {"location": data['geocodes'][0]['location']
#            , "province": data['geocodes'][0]['province']
#            , "city": data['geocodes'][0]['city']
#            , "district": data['geocodes'][0]['district']
#            , "formatted_address": data['geocodes'][0]['formatted_address']
#            }
    return data

def getId(city, district, address):
    url = "https://restapi.amap.com/v3/place/text?key={0}&citylimit=true&output=json&keywords={1}&city={2}".format(keys[currkey], address, city)
    idreq = requests.get(url=url)
    reqdata = idreq.json()
    if reqdata["status"] == "0":
        return reqdata
    pois = reqdata["pois"]
    for p in pois:
        if p["name"] in address and p["adname"] == district:
            print("OK")
            return {"name": p["name"], "Id": p["id"]}
        elif (p["name"] in address or address in p["name"]) and p["adname"] == district:
            print("OK, But District msg lost...")
            return {"name": p["name"], "Id": p["id"]}
        elif (p["name"] in address or address in p["name"]) and district == "":
            print("OK, But District msg lost...")
            return {"name": p["name"], "Id": p["id"], "address": p["address"]}
    return {"orgname": address, "name": pois[0]["name"], "Id": pois[0]["id"], "address": pois[0]["address"]}

def getshape(geojson):
    spec = geojson["data"]["spec"]["mining_shape"]["shape"].split(";")
    polygon = []
    for s in spec:
        polygon.append(list(GCJ2WGS(s)))
    
    return polygon
    

"""Parameters For idurl
key=4b86820a7590de60e4f81f53e59ae17f
&citylimit=true&output=json
&keywords=%E4%B8%AD%E6%B5%B7%E9%BE%99%E6%B9%BE%E5%9B%BD%E9%99%85%E8%8A%B1%E5%9B%AD
&city=%E4%B8%AD%E5%B1%B1
"""
idurl = "https://restapi.amap.com/v3/place/text?"
shapeurl = "https://ditu.amap.com/detail/get/detail?"  # id=B02F8037YI
xiaoqus = pd.ExcelFile("E:/Documents/2019-nCoV/2019-nCoV_Xiaoqu_WuHanShequ.xlsx").parse(sheet_name="xiaoqu_0209", header=1,index_col=None,dtype=object).fillna("")
xiaoqud = xiaoqus.to_dict(orient="records")
#address = "".join([xiaoqud[0]["province"], xiaoqud[0]["city"], xiaoqud[0]["district"], xiaoqud[0]["name"]])
#city = xiaoqud[0]["city"]

#id_data = {
#        "city": city
#        , "keyword": xiaoqud[0]["name"]
#        , "citylimit": "true"
#        , "output": "json"
#        , "key": keys[currkey]
#        }

#idreq = requests.get(url=idurl+urlencode(id_data))
#idd = idreq.json()
#geodata = geocode({"city": xiaoqud[0]["city"], "address": address})

# para:
# key={2}
# &address={0}
# &output=json
# &city={1}
#geopara = {
#        "key": keys[currkey]
#        , "address": "中山市石岐区兴利路3号中海龙湾国际"
#        , "output": "json"
#        , "city": "中山市"
#        }
#geourl = 'https://restapi.amap.com/v3/geocode/geo?'+urlencode(geopara)
#url = "https://ditu.amap.com/detail/get/detail?id=B001B0I9FL"
#georeq = requests.get(url=url, headers=headers)
#geojson = georeq.json()
#polygon = getshape(geojson)
#point = [{"type": "Feature"
#        , "geometry": {"type": "Polygon"
#                       , "coordinates": [polygon]
#                }
#        , "properties": {
#                "city": "武汉市"
#                , "province": "湖北省"
#                , "district": "江岸区"
#                , "name": "东方明珠"
#                , "address": "湖北省武汉市江岸区后湖街兴业南路7号"
#                }
#        }]

points = []
noneIdp = []
finish = []
for a in tqdm(xiaoqud):
    if a["name"] in finish:
        continue
    print(a["city"], a["district"], a["name"])
    Id = getId(a["city"], a["district"], a["name"])
    if "status" in Id and Id["status"] == "0":
        print("None Id, ",Id)
        noneIdp.append({"city": a["city"], "district": a["district"], "name": a["name"]})
        continue
    shpurl = "https://ditu.amap.com/detail/get/detail?id={0}".format(Id["Id"])
    geo = requests.get(url=shpurl, headers=headers2)
    geojson = geo.json()
    while "url" in geojson:
        print("https://ditu.amap.com"+geojson["url"])
        check = print("有验证码,请解锁验证码")
        time.sleep(10)
        if check == "ok":
            geojson = requests.get(url=shpurl, headers=headers2).json()
            break
        else:
            geojson = requests.get(url=shpurl, headers=headers2).json()
            
    polygon = getshape(geojson)
    point = {"type": "Feature"
        , "geometry": {"type": "Polygon"
                       , "coordinates": [polygon]
                }
        , "properties": {
                "city": a["city"]
                , "province": a["province"]
                , "district": a["district"]
                , "name": Id["name"]
                , "address": Id["address"]
                }
        }
    points.append(point)
    time.sleep(0.4)
    finish.append(a["name"])