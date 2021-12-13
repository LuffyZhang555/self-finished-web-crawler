import pandas as pd
import string
from unicodedata import name
import requests
import json
import numpy
import time
import random
from datetime import date
import os
import logging
import logging.config
import re


thisdate=time.strftime("%Y-%m-%d")
filename = 'Fulffy_Report' + thisdate + '.csv'
textname = 'Fullfy_failure Report'+ thisdate + '.txt'

LOG_PATH = "logs/" + thisdate + '.log'
#logging.config.fileConfig("spider_logging.conf")
logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', handlers=[logging.FileHandler(LOG_PATH, encoding='utf-8')], level=logging.DEBUG)
#logger=logging.getLogger(__name__)
logging.getLogger().addHandler(logging.StreamHandler())
logging.info('main starts')

d1 = time.strftime("%Y-%m-%d %H:%M:%S")

majorlist=["AUSTRILIA","GERMANY","FRANCE","ITALY","UNITED KINGDOM","UNITED STATES","CANADA","CHINA","JAPAN","SINGAPORE","TAIWAN","KOREA"]
url2="https://www.fulffy.com/api/extApi/getShippingResult"
outdir = '../data/'
payload={
    "country": "AUSTRALIA",
    "package_type": "parcel",
    "act_weight": "22",
    "vol_weight": "0.4",
    "length": "20",
    "width": "10",
    "height": "10",
    "toggle": "one",
    "export_country": "HONG KONG",
    "calculator": "Y",
    "token": "c36f5fed1bfbb97f7fb3986916d54d24",
    "lang": "",
    "cache_timestamp": 1637564062262
    
}
shortcode={
    
    "Austria": "AT",
    "AUSTRILIA":"AU",
    "Belgium":"BE",
    "Bulgaria":"BG",
    "Croatia":"HR",
    "Czech Republic": "CZ",
    "Denmark":"DK",
    "Estonia":"EE",
    "Finland":"FI",
    "FRANCE":"FR",
    "GERMANY":'DE',
    "Greece":"GR",
    "Hungary":"HU",
    "Ireland":"IE",
    "ITALY":"IT",
    "Latvia":"LV",
    "Lithuania":"LT",
    "Luxembourg":"LU",
    "NETHERLANDS":"NL",
	"NEW ZEALAND":"NZ",
	"Poland":"PL",
	"Portugal":"PT",
	"Romania":"RO",
	"Slovakia":"SK",
	"Slovenia":"SI",
	"Spain":"ES",
	"Sweden":"SE",
	"UNITED KINGDOM":"GB",
	"UNITED STATES":"US",
    "HongKong" :"HK",
    "CHINA" :"CN",
    "CANADA":"CA",
    "JAPAN":"JP",
    "KOREA":"KR",
    "SINGAPORE":"SG",
    "TAIWAN":"TW",
    "MALAYSIA":"MY"
}

column_names = ["platform","service_provider", "size_of_item(cm)","weight(kg)", "origin" , "destination","value(hkd)","record_date_time(hkt)", "max_transit_days","min_transit_days","pickup_service"]
df = pd.DataFrame(columns = column_names)

'''
r2=requests.get(url=url2,params=payload)
s=r2.text
soup1 = BeautifulSoup(s)
soup2=soup1.find_all(class_="font-bold md:text-xl flex flex-row items-center") 
soup3=soup1.find_all(class_="font-bold text-lg md:text-2xl leading-tight mt-1 whitespace-nowrap")
soup4=soup1.find_all(class_="ri-time-line mr-2")
obj = re.compile(r'<button class="text-xs border border-gray-200 text-gray-600 flex flex-row rounded my-1 px-1 leading-relaxed modalHelpCenter ml-2 whitespace-nowrap" data-id="10">\n<span>(?P<test>.*?)</span>',re.S)
obj2=re.compile(r'<span class="whitespace-nowrap">\n(?P<serviceprovider>.*?)</span>\n\n</div>',re.S)
obj3=re.compile(r'<div class="font-bold text-lg md:text-2xl leading-tight mt-1 whitespace-nowrap">(?P<value>.*?) HKD</div>\n<div class',re.S)
obj4=re.compile(r'\n<i class="ri-time-line mr-2"></i><span>é è¨ˆ (?P<min>.*?)-(?P<max>.*?) æ—¥åˆ°é”</span>',re.S )
res = obj.findall(s)
res2 = obj2.findall(s)
res3 = obj3.findall(s)
res4 = obj4.findall(s)
'''
index=0
error_number=0
def getdata(k,j,index,error_number):# set origin country is HK weight 0-20kg
    payload["country"]=majorlist[k]
    payload["export_country"] ="HONG KONG"
    weight=j*0.5  
    
    payload["act_weight"]=weight
    r=callapi(payload)
    try :
        s=r.text
        print('success')
    except :
        time.sleep( random.randint(10,29) ) 
        print("not html")  
        error_number=error_number+1 
        getdata(k,j,index,error_number)    
        
        
    if (r.status_code==200):
        #soup1 = BeautifulSoup(s)
        #soup2=soup1.find_all(class_="font-bold md:text-xl flex flex-row items-center") 
        #soup3=soup1.find_all(class_="font-bold text-lg md:text-2xl leading-tight mt-1 whitespace-nowrap")
        #soup4=soup1.find_all(class_="ri-time-line mr-2")
        obj = re.compile(r'<button class="text-xs border border-gray-200 text-gray-600 flex flex-row rounded my-1 px-1 leading-relaxed modalHelpCenter ml-2 whitespace-nowrap" data-id="10">\n<span>(?P<test>.*?)</span>',re.S)
        obj2=re.compile(r'<span class="whitespace-nowrap">\n(?P<serviceprovider>.*?)</span>\n\n</div>',re.S)
        obj3=re.compile(r'<div class="font-bold text-lg md:text-2xl leading-tight mt-1 whitespace-nowrap">(?P<value>.*?) HKD</div>\n<div class',re.S)
        obj4=re.compile(r'\n<i class="ri-time-line mr-2"></i><span>é è¨ˆ (?P<min>.*?)-(?P<max>.*?) æ—¥åˆ°é”</span>',re.S )
        res = obj.findall(s)
        res2 = obj2.findall(s)
        res3 = obj3.findall(s)
        res4 = obj4.findall(s)
        total=len(res2)
        for l in range(0,total):
            df.loc[index]=["Fulffy",res2[l],"20*10*10",weight,"HK",shortcode[majorlist[k]],res3[l],d1,res4[l][1],res4[l][0],True]
            index=index+1
    else:
        print('error')
        error_number=error_number+1
        time.sleep( random.randint(10,19) )
        getdata(k,j,index,error_number)
    return index,error_number


def getdata2(k,j,index,error_number):# set origin country is HK weight 0-20kg
    payload["country"]="HONG KONG"
    payload["export_country"]=majorlist[k]
    weight=j*0.5  
    
    payload["act_weight"]=weight
    r=callapi(payload)
    try :
        s=r.text
        print('success')
    except :
        time.sleep( random.randint(10,29) ) 
        print("not html")  
        error_number=error_number+1 
        getdata(k,j,index,error_number)    
        
        
    if (r.status_code==200):
        #soup1 = BeautifulSoup(s)
        #soup2=soup1.find_all(class_="font-bold md:text-xl flex flex-row items-center") 
        #soup3=soup1.find_all(class_="font-bold text-lg md:text-2xl leading-tight mt-1 whitespace-nowrap")
        #soup4=soup1.find_all(class_="ri-time-line mr-2")
        obj = re.compile(r'<button class="text-xs border border-gray-200 text-gray-600 flex flex-row rounded my-1 px-1 leading-relaxed modalHelpCenter ml-2 whitespace-nowrap" data-id="10">\n<span>(?P<test>.*?)</span>',re.S)
        obj2=re.compile(r'<span class="whitespace-nowrap">\n(?P<serviceprovider>.*?)</span>\n\n</div>',re.S)
        obj3=re.compile(r'<div class="font-bold text-lg md:text-2xl leading-tight mt-1 whitespace-nowrap">(?P<value>.*?) HKD</div>\n<div class',re.S)
        obj4=re.compile(r'\n<i class="ri-time-line mr-2"></i><span>é è¨ˆ (?P<min>.*?)-(?P<max>.*?) æ—¥åˆ°é”</span>',re.S )
        res = obj.findall(s)
        res2 = obj2.findall(s)
        res3 = obj3.findall(s)
        res4 = obj4.findall(s)
        total=len(res2)
        for l in range(0,total):
            df.loc[index]=["Fulffy",res2[l],"20*10*10",weight,"HK",shortcode[majorlist[k]],res3[l],d1,res4[l][1],res4[l][0],True]
            index=index+1
    else:
        print('error')
        error_number=error_number+1
        time.sleep( random.randint(10,19) )
        getdata(k,j,index,error_number)
    return index,error_number


def getdata3(k,j,index,error_number):# set origin country is HK weight 0-20kg
    payload["country"]=majorlist[k]
    payload["export_country"] ="HONG KONG"
    weight=30+j*10
    payload["act_weight"]=weight
    r=callapi(payload)
    try :
        s=r.text
        print('success')
    except :
        time.sleep( random.randint(10,29) ) 
        print("not html")  
        error_number=error_number+1 
        getdata(k,j,index,error_number)    
        
        
    if (r.status_code==200):
        #soup1 = BeautifulSoup(s)
        #soup2=soup1.find_all(class_="font-bold md:text-xl flex flex-row items-center") 
        #soup3=soup1.find_all(class_="font-bold text-lg md:text-2xl leading-tight mt-1 whitespace-nowrap")
        #soup4=soup1.find_all(class_="ri-time-line mr-2")
        obj = re.compile(r'<button class="text-xs border border-gray-200 text-gray-600 flex flex-row rounded my-1 px-1 leading-relaxed modalHelpCenter ml-2 whitespace-nowrap" data-id="10">\n<span>(?P<test>.*?)</span>',re.S)
        obj2=re.compile(r'<span class="whitespace-nowrap">\n(?P<serviceprovider>.*?)</span>\n\n</div>',re.S)
        obj3=re.compile(r'<div class="font-bold text-lg md:text-2xl leading-tight mt-1 whitespace-nowrap">(?P<value>.*?) HKD</div>\n<div class',re.S)
        obj4=re.compile(r'\n<i class="ri-time-line mr-2"></i><span>é è¨ˆ (?P<min>.*?)-(?P<max>.*?) æ—¥åˆ°é”</span>',re.S )
        res = obj.findall(s)
        res2 = obj2.findall(s)
        res3 = obj3.findall(s)
        res4 = obj4.findall(s)
        total=len(res2)
        for l in range(0,total):
            df.loc[index]=["Fulffy",res2[l],"20*10*10",weight,"HK",shortcode[majorlist[k]],res3[l],d1,res4[l][1],res4[l][0],True]
            index=index+1
    else:
        print('error')
        error_number=error_number+1
        time.sleep( random.randint(10,19) )
        getdata(k,j,index,error_number)
    return index,error_number


def getdata4(k,j,index,error_number):# set origin country is HK weight 0-20kg
    payload["country"]="HONG KONG"
    payload["export_country"]=majorlist[k]
    weight=30+j*10 
    payload["act_weight"]=weight
    r=callapi(payload)
    try :
        s=r.text
        print('success')
    except :
        time.sleep( random.randint(10,29) ) 
        print("not html")  
        error_number=error_number+1 
        getdata(k,j,index,error_number)    
        
        
    if (r.status_code==200):
        #soup1 = BeautifulSoup(s)
        #soup2=soup1.find_all(class_="font-bold md:text-xl flex flex-row items-center") 
        #soup3=soup1.find_all(class_="font-bold text-lg md:text-2xl leading-tight mt-1 whitespace-nowrap")
        #soup4=soup1.find_all(class_="ri-time-line mr-2")
        obj = re.compile(r'<button class="text-xs border border-gray-200 text-gray-600 flex flex-row rounded my-1 px-1 leading-relaxed modalHelpCenter ml-2 whitespace-nowrap" data-id="10">\n<span>(?P<test>.*?)</span>',re.S)
        obj2=re.compile(r'<span class="whitespace-nowrap">\n(?P<serviceprovider>.*?)</span>\n\n</div>',re.S)
        obj3=re.compile(r'<div class="font-bold text-lg md:text-2xl leading-tight mt-1 whitespace-nowrap">(?P<value>.*?) HKD</div>\n<div class',re.S)
        obj4=re.compile(r'\n<i class="ri-time-line mr-2"></i><span>é è¨ˆ (?P<min>.*?)-(?P<max>.*?) æ—¥åˆ°é”</span>',re.S )
        res = obj.findall(s)
        res2 = obj2.findall(s)
        res3 = obj3.findall(s)
        res4 = obj4.findall(s)
        total=len(res2)
        for l in range(0,total):
            df.loc[index]=["Fulffy",res2[l],"20*10*10",weight,"HK",shortcode[majorlist[k]],res3[l],d1,res4[l][1],res4[l][0],True]
            index=index+1
    else:
        print('error')
        error_number=error_number+1
        time.sleep( random.randint(10,19) )
        getdata(k,j,index,error_number)
    return index,error_number


def callapi(payload):
    time.sleep( random.randint(10,19) )
    payload2=payload
    r=requests.get(url=url2,params=payload2)
    return r

for k in range(0,12):
    for j in range(1,41):
        print("1-",k,"-",j)
        logging.info("still on first set")
        try:
            index,error_number=getdata(k,j,index,error_number)
            logging.info("right now it finished 1- %d - %d ",k,j)
        except Exception:
            logging.info(Exception)

for k in range(0,12):
    for j in range(1,41):
        print("2-","-",j)
        logging.info("2-",k,"-",j)
        try:
            index,error_number=getdata2(k,j,index,error_number)
            logging.info("right now it finished 2- %d - %d ",k,j)
        except Exception:
            logging.info(Exception)
for k in range(0,12):
    for j in range(0,28):
        print("3-",k,"-",j)
        logging.info("3-",k,"-",j)
        try:
            index,error_number=getdata3(k,j,index,error_number)
            logging.info("right now it finished 3- %d - %d ",k,j)
        except Exception:
            logging.info(Exception)
for k in range(0,12):
    for j in range(0,28):
        print("4-",k,"-",j)
        logging.info("4-",k,"-",j)
        try:
            index,error_number=getdata4(k,j,index,error_number)
            logging.info("right now it finished 4- %d - %d ",k,j)
        except Exception:
            logging.info(Exception)
'''
for l in range (0,len(res2)):
    df.loc[index]=["fulffy",res2[l],"20*10*10","22","HK","AU",res3[l],d1,res4[l][1],res4[l][0],True]
    index=index+1
'''    
df['value(hkd)']=df['value(hkd)'].str.extract('(\d+)')    
#df.to_csv("C:/Users/Luffy Zhang/Desktop/fulffyv1.0_2021.12.6.csv",index=False) 
df.to_csv(os.path.join(outdir, filename), index=False)

