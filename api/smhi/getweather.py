#!/usr/bin/python2.7
import sys
import json
from requests import get, post
import argparse
from time import sleep
#Vasteras
#59.6198 16.6119
#Parameter Unit      Level-Type Level(m) Description                             Value-Range  
#msl       hPa       hmsl       0        Air pressure                            Decimal number, one decimal
#t         C         hl         2        Air temperature                         Decimal number, one decimal
#vis       km        hl         2        Horizontal visibility                   Decimal number, one decimal
#wd        degree    hl         10       Wind direction                          Integer
#ws        m/s       hl         10       Wind speed                              Decimal number, one decimal
#r         %         hl         2        Relative humidity                       Integer, 0-100
#tstm      %         hl         0        Thunder probability                     Integer, 0-100
#tcc_mean  octas     hl         0        Mean value of total cloud cover         Integer, 0-8
#lcc_mean  octas     hl         0        Mean value of low level cloud cover     Integer, 0-8
#mcc_mean  octas     hl         0        Mean value of medium level cloud cover  Integer, 0-8
#hcc_mean  octas     hl         0        Mean value of high level cloud cover    Integer, 0-8
#gust      m/s       hl         10       Wind gust speed                         Decimal number, one decimal
#pmin      mm/h      hl         0        Minimum precipitation intensity         Decimal number, one decimal
#pmax      mm/h      hl         0        Maximum precipitation intensity         Decimal number, one decimal
#spp       %         hl         0        Percent of precipitation in frozen form Integer, -9 or 0-100
#pcat      category  hl         0        Precipitation category                  Integer, 0-6
#pmean     mm/h      hl         0        Mean precipitation intensity            Decimal number, one decimal
#pmedian   mm/h      hl         0        Median precipitation intensity          Decimal number, one decimal
#Wsymb2    code      hl         0        Weather symbol                          Integer, 1-27 (1-15 for pmp2g)

    #    {
    #        "levelType": "hl", 
    #        "values": [
    #                    80
    #                      ], 
    #        "name": "r", 
    #        "unit": "percent", 
    #        "level": 2
    #                                                                                }, 

# https://opendata.smhi.se/apidocs/metfcst/parameters.html
def get_weather(latitude=59.6198,longitude=16.6119, update=False):
    print("latitude:{}, longitude:{}".format(latitude,longitude))
    url = "https://opendata-download-metfcst.smhi.se/api/category/pmp3g/version/2/geotype/point/lon/{}/lat/{}/data.json".format(longitude, latitude)
    headers = {'content-type': 'application/json'}

    if update: 
        response = get(url, headers=headers)
        states = json.loads(response.text)
        print(json.dumps(states, indent=4, sort_keys=True))
    else: 
        json_data = open("data.log").read()
        data = json.loads(json_data)
       # print(json.dumps(data['timeSeries'][0], indent=4))
       # print("not updating")

        #FIXME: percipitation category stuff, check documentation
        for attributes in data['timeSeries'][0]['parameters']:
            for param in ["t", "ws", "pcat", "Wsmb2"]:
                #print(param)
                #print(attributes)
                if param == attributes['name']:
                    name = mapping(param)
                    value = attributes['values']
                    unit = attributes['unit']
                    print("{}: {} {}\n".format(name, value, unit))
  #  for item in states:
  #      if item['entity_id'] == entity_id:
  #          #print(item)
  #          return item
def mapping(parameter):
    description_list = {
       "msl":" Air pressure",                                                      
       "t":" Air temperature",     
       "vis":" Horizontal visibility",
       "wd":" Wind direction",    
       "ws":" Wind speed",         
       "r":" Relative humidity",    
       "tstm":" Thunder probability",      
       "tcc_mean":" Mean value of total cloud cover",  
       "lcc_mean":" Mean value of low level cloud cover",  
       "mcc_mean":" Mean value of medium level cloud cover",
       "hcc_mean":" Mean value of high level cloud cover",  
       "gust":" Wind gust speed",                  
       "pmin":" Minimum precipitation intensity",      
       "pmax":" Maximum precipitation intensity",      
       "spp":" Percent of precipitation in frozen form", 
       "pcat":" Precipitation category",   
       "pmean":" Mean precipitation intensity", 
       "pmedian":" Median precipitation intensity",
       "Wsymb2":" Weather symbol", 
    }
    try:
        parameter = description_list[parameter]
    except Exception:
        parameter = "unknown description"
        
    return parameter 

if __name__ == '__main__':
    get_weather()
