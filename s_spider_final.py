import string
import pandas as pd
import logging
import logging.config

from unicodedata import name
import requests
import json
import numpy
import time
import random
from datetime import date
import os



thisdate=time.strftime("%Y-%m-%d")
LOG_PATH = "logs/" + thisdate + '.log'
logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', handlers=[logging.FileHandler(LOG_PATH, encoding='utf-8')], level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())
logging.info('main starts')

d1 = time.strftime("%Y-%m-%d %H:%M:%S")

column_names = ["platform","service_provider", "size_of_item(cm)", "weight(kg)","origin", "destination","value(hkd)", "record_date_time(hkt)", "max_transit_days","min_transit_days","pickup_service","free_pickup","paid_pickup","pickup_fee","noservcie"]
df = pd.DataFrame(columns = column_names)
toCountrylist=["AU","DE","FR","IT","JP","CA","CN","GB","US","KR","SG","TW"]###i-->country
#toCountrylist=["AT","AU","BE","CA","CN","JP","DE","DK","ES","FR","IT","NL","NZ","PL","PT","GB","US","KR","MY","SG","TH","TW","VN"]###i-->country
weightlist=[0.5,1,1.5,2,5,10,15,20,25,30]###j-->Weight
                        ###k-->number of data result

outdir = '../data/'
filename = 'Spaceship_Report' + thisdate + '.csv'
textname = 'Spaceship_failure Report'+ thisdate + '.txt'
url="https://panel.spaceship.hk/api/quotations"
headers={
    "accept": "application/json",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "x-locale": "en-hk"
}
error_number=0
index=0
json1={"fromCountry":"HK","toCountry":"US","totalWeight":"1.7","boxes":[{"boxType":"largeBox","length":"20","width":"10","height":"10","quantity":"1"}]}

###from HK
def getdata(k,j,index,error_number):
    weight=j*0.5  
    json1["toCountry"]=toCountrylist[k]
    json1["totalWeight"]=weight
    r=callapi(json1)
    try :
        data=r.json()
        print('success')
    except :
        time.sleep( random.randint(10,29) ) 
        print("not Json")  
        error_number=error_number+1 
        getdata(k,j,index,error_number)    
        
        
    if (r.status_code==200) & ('data'in data):
        
        total=len(data['data'])
        for l in range(0,total):
            a =  "pickupFee" in data['data'][l]
            if a==True:
                pickupfree=False
                pickupfee=data['data'][l]['naturalAmount']['pickupFee']
            if a==False:
                pickupfree=True
                pickupfee=0

            df.loc[index]=["Spaceship",data['data'][l]['slug'],"20*10*10",weight,"HK",toCountrylist[k],data['data'][l]['naturalAmount']['totalRate'],d1,data['data'][l]['maxDeliveryDays'],data['data'][l]['minDeliveryDays'],True,pickupfree,a,pickupfee,data['data'][l]['noService']]
            index=index+1
    else:
        print('error')
        error_number=error_number+1
        time.sleep( random.randint(10,19) )
        getdata(k,j,index,error_number)
    return index,error_number
###to HK    
def getdata2(k,j,index,error_number):
    weight=j*0.5
    json1["toCountry"]="HK"  
    json1["fromCountry"]=toCountrylist[k]
    json1["totalWeight"]=weight
    r=callapi(json1)
    trytime=0
    try :
        data=r.json()
        print('success')
    except :
        time.sleep( random.randint(10,29) ) 
        print("not Json")  
        error_number=error_number+1 
        if trytime==0:
            getdata(k,j,index,error_number)    
        
    if (r.status_code==200) & ('data'in data):
        
        total=len(data['data'])
        for l in range(0,total):
            a =  "pickupFee" in data['data'][l]
            if a==True:
                pickupfree=False
                pickupfee=data['data'][l]['naturalAmount']['pickupFee']
            if a==False:
                pickupfree=True
                pickupfee=0

            df.loc[index]=["Spaceship",data['data'][l]['slug'],"20*10*10",weight,toCountrylist[k],"HK",data['data'][l]['naturalAmount']['totalRate'],d1,data['data'][l]['maxDeliveryDays'],data['data'][l]['minDeliveryDays'],True,pickupfree,a,pickupfee,data['data'][l]['noService']]
            index=index+1
    else:
        print('error')
        error_number=error_number+1
        time.sleep( random.randint(10,19) )
        getdata2(k,j,index,error_number)
        
    return index,error_number
###from HK to other 30-300kg    
def getdata3(k,j,index,error_number):
    weight=30+j*10  
    json1["fromCountry"]="HK"
    json1["toCountry"]=toCountrylist[k]
    json1["totalWeight"]=weight
    r=callapi(json1)
    try :
        data=r.json()
        print('success')
    except :
        time.sleep( random.randint(10,29) ) 
        print("not Json")  
        error_number=error_number+1 
        getdata(k,j,index,error_number)    
       
    if (r.status_code==200) & ('data'in data):
        
        total=len(data['data'])
        for l in range(0,total):
            a =  "pickupFee" in data['data'][l]
            if a==True:
                pickupfree=False
                pickupfee=data['data'][l]['naturalAmount']['pickupFee']
            if a==False:
                pickupfree=True
                pickupfee=0

            df.loc[index]=["Spaceship",data['data'][l]['slug'],"20*10*10",weight,"HK",toCountrylist[k],data['data'][l]['naturalAmount']['totalRate'],d1,data['data'][l]['maxDeliveryDays'],data['data'][l]['minDeliveryDays'],True,pickupfree,a,pickupfee,data['data'][l]['noService']]
            index=index+1
    else:
        print('error')
        error_number=error_number+1
        time.sleep( random.randint(10,19) )
        getdata(k,j,index,error_number)
        
    return index,error_number

###from other to HK 30-300kg
def getdata4(k,j,index,error_number):
    weight=30+j*10
    json1["toCountry"]="HK"  
    json1["fromCountry"]=toCountrylist[k]
    json1["totalWeight"]=weight
    r=callapi(json1)
    try :
        data=r.json()
        print('success')
    except :
        time.sleep( random.randint(10,29) ) 
        print("not Json")  
        error_number=error_number+1 
        getdata(k,j,index,error_number)    
       
    if (r.status_code==200) & ('data'in data):
        
        total=len(data['data'])
        for l in range(0,total):
            a =  "pickupFee" in data['data'][l]
            if a==True:
                pickupfree=False
                pickupfee=data['data'][l]['naturalAmount']['pickupFee']
            if a==False:
                pickupfree=True
                pickupfee=0

            df.loc[index]=["Spaceship",data['data'][l]['slug'],"20*10*10",weight,toCountrylist[k],"HK",data['data'][l]['naturalAmount']['totalRate'],d1,data['data'][l]['maxDeliveryDays'],data['data'][l]['minDeliveryDays'],True,pickupfree,a,pickupfee,data['data'][l]['noService']]
            index=index+1
    else:
        print('error')
        error_number=error_number+1
        time.sleep( random.randint(10,19) )
        getdata2(k,j,index,error_number)
        
    return index,error_number

  
def callapi(json):
    time.sleep( random.randint(5,15) )
    json1=json
    r = requests.post(url, json=json1)
    return r

for k in range(0,12):
    for j in range(1,41):
        print(k,"-",j)
        trytime=0
        try:
            index,error_number=getdata(k,j,index,error_number)
            logging.info("right now it finished 1- %d - %d ",k,j)
        except Exception:
            if trytime==0:
                logging.info(Exception)
                trytime=trytime+1
                try:
                    index,error_number=getdata(k,j,index,error_number)
                except Exception:
                    logging.info(Exception)
            else:
                logging.info(Exception)
            

for k in range(0,12):
    for j in range(1,41):
        print(k,"-",j)
        try:
            index,error_number=getdata2(k,j,index,error_number)
            logging.info("right now it finished 1- %d - %d ",k,j)
        except Exception:
            if trytime==0:
                logging.info(Exception)
                trytime=trytime+1
                try:
                    index,error_number=getdata(k,j,index,error_number)
                except Exception:
                    logging.info(Exception)
            else:
                logging.info(Exception)    

for k in range(0,12):
    for j in range(0,28):
        print(k,"-",j)
        try:
            index,error_number=getdata3(k,j,index,error_number)
            logging.info("right now it finished 1- %d - %d ",k,j)
        except Exception:
            if trytime==0:
                logging.info(Exception)
                trytime=trytime+1
                try:
                    index,error_number=getdata(k,j,index,error_number)
                except Exception:
                    logging.info(Exception)
            else:
                logging.info(Exception)  
  
for k in range(0,12):
    for j in range(0,28):
        print(k,"-",j)
        try:
            index,error_number=getdata4(k,j,index,error_number)
            logging.info("right now it finished 1- %d - %d ",k,j)
        except Exception:
            if trytime==0:
                logging.info(Exception)
                trytime=trytime+1
                try:
                    index,error_number=getdata(k,j,index,error_number)
                except Exception:
                    logging.info(Exception)
            else:
                logging.info(Exception)  

df1=df[df["noservcie"]==False]

df1=df1.drop(columns=['noservcie'])
df1.to_csv(os.path.join(outdir, filename), index=False)
#df1.to_csv("C:/Users/Luffy Zhang/Desktop/spaceshiptestv2.0_2021.12.1.csv",mode='w',index=False) 























