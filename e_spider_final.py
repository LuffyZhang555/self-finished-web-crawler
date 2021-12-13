import logging
import logging.config
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

thisdate=time.strftime("%Y-%m-%d")

LOG_PATH = "logs/" + thisdate + '.log'
logging.basicConfig(format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s', datefmt='%H:%M:%S', handlers=[logging.FileHandler(LOG_PATH, encoding='utf-8')], level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())
logging.info('main starts')
d1 = time.strftime("%Y-%m-%d %H:%M:%S")
filename = 'Easyship_Report' + thisdate + '.csv'
textname = 'Easyship_failure Report'+ thisdate + '.txt'
weightlist=[0.5,1,1.5,2,2.5,4,10,15,20,25,30]
column_names = ["platform","service_provider", "size_of_item(cm)","weight(kg)", "origin" , "destination","value(hkd)","record_date_time(hkt)", "max_transit_days","min_transit_days","available_handover_options"]
df = pd.DataFrame(columns = column_names)
url="https://api.easyship.com/api/v1/get_all_rates"
#weightlist=[0.5,1,1.5,2,2.5,3,3.5]
headers={
    "authorization": "Bearer OGHF340uM56ftCcAiLA6Dw"
}
testlist=["Australia","Germany","France","Italy","UK","US","Canada","China","Japan","Taiwan","Singapore","Korea"]
jsontest={
    "useExistingAddress": False, 
    "origin_country_id": 96, 
    "origin_postal_code": "", 
    "origin_address_id":"" , 
    "incoterms": "DDU", 
    "is_insured": False, 
    "items": [
        {
            "declared_currency": "HKD", 
            "category_id": 14, 
            "actual_weight": 50, 
            "declared_customs_value": "100"
        }
    ], 
    "residential_surcharge": {
        "calculate": True, 
        "apply_to_total_charge": False
    }, 
    "origin_country": {
        "id": 96, 
        "name": "Hong Kong", 
        "simplified_name": "Hong Kong", 
        "alpha2": "HK", 
        "alpha3": "HKG", 
        "number": "344", 
        "country_code": "852", 
        "continent": "Asia", 
        "region": "Asia", 
        "subregion": "Eastern Asia", 
        "currency_code": "HKD", 
        "currency_symbol": "$", 
        "display_currency": "HKD", 
        "requirements": {
            "requires_state": False, 
            "has_postal_code": False, 
            "postal_code_regex": "", 
            "postal_code_examples": "", 
            "postal_code_mandatory_from_origin": "", 
            "consignee_tax_id_required": False, 
            "consignee_tax_id_required_umbrella_names": [ ]
        }
    }, 
    "destination_country": {
        "id": 234, 
        "name": "United States", 
        "simplified_name": "United States", 
        "alpha2": "US", 
        "alpha3": "USA", 
        "number": "840", 
        "country_code": "1", 
        "continent": "North America", 
        "region": "Americas", 
        "subregion": "Northern America", 
        "currency_code": "USD", 
        "currency_symbol": "$", 
        "display_currency": "$", 
        "requirements": {
            "requires_state": True, 
            "has_postal_code": True, 
            "postal_code_regex": "^[0-9]{5}$", 
            "postal_code_examples": "99999", 
            "postal_code_mandatory_from_origin": [
                39, 
                234
            ], 
            "consignee_tax_id_required": False, 
            "consignee_tax_id_required_umbrella_names": [ ]
        }
    }, 
    "destination_postal_code": "", 
    "destination_state": "", 
    "destination_city": "", 
    "box": {
        "name": "Custom Box", 
        "height": "20", 
        "width": "10", 
        "length": "10", 
        "is_box_fitted": False
    }, 
    "destination_country_id": 234, 
    "company_id": "c26e7ce1-783c-4c98-894d-35d27786539d", 
    "excluded_courier_admin_names": [
        "AWX_HK", 
        "AWX_CN"
    ]
}

countrycode={
    
    "Austria": 13,
    "Australia":14,
    "Belgium":21,
    "Bulgaria":23,
    "Croatia":99,
    "Czech Republic": 57,
    "Denmark":60,
    "Estonia":65,
    "Finland":71,
    "France":76,
    "Germany":58,
    "Greece":90,
    "Hungary":101,
    "Ireland":103,
    "Italy":111,
    "Latvia":136,
    "Lithuania":134,
    "Luxembourg":135,
    "Netherlands":167,
	"New Zealand":172,
	"Poland":180,
	"Portugal":185,
	"Romania":190,
	"Slovakia":203,
	"Slovenia":201,
	"Spain":69,
	"Sweden":198,
	"UK":78,
	"US":234,
    "HongKong":96,
    "China":49,
    "Canada":39,
    "Japan":115,
    "Malaysia":159,
    "Singapore":199,
    "Taiwan":229,
    "Korea":123

}
#majorlist=["Austria","Australia","Belgium","Denmark","Spain","France","Italy","Netherlands","New Zealand","Poland","Portugal","UK","US","Germany","HongKong"]
shortcode={
    
    "Austria": "AT",
    "Australia":"AU",
    "Belgium":"BE",
    "Bulgaria":"BG",
    "Croatia":"HR",
    "Czech Republic": "CZ",
    "Denmark":"DK",
    "Estonia":"EE",
    "Finland":"FI",
    "France":"FR",
    "Germany":'DE',
    "Greece":"GR",
    "Hungary":"HU",
    "Ireland":"IE",
    "Italy":"IT",
    "Latvia":"LV",
    "Lithuania":"LT",
    "Luxembourg":"LU",
    "Netherlands":"NL",
	"New Zealand":"NZ",
	"Poland":"PL",
	"Portugal":"PT",
	"Romania":"RO",
	"Slovakia":"SK",
	"Slovenia":"SI",
	"Spain":"ES",
	"Sweden":"SE",
	"UK":"GB",
	"US":"US",
    "HongKong" :"HK",
    "China" :"CN",
    "Canada":"CA",
    "Japan":"JP",
    "Korea":"KR",
    "Singapore":"SG",
    "Taiwan":"TW",
    "Malaysia":"MY",
    "Korea":"KR"
}

index=0

#available_handover_options
weightid=1
error_number=0

def getdata(k,j,index,error_number):# set origin country is HK weight 0-20kg
    jsontest["origin_country_id"]=96  
    weight=j*0.5  
    jsontest["destination_country_id"]=countrycode[testlist[k]]
    jsontest["items"][0]["actual_weight"]=weight
    r=callapi(jsontest)
    try :
        data=r.json()
        print('success')
    except :
        time.sleep( random.randint(10,29) ) 
        print("not Json")  
        error_number=error_number+1 
        getdata(k,j,index,error_number)    
        
        
    if (r.status_code==200) & ('rates'in data):
        
        total=len(data['rates'])
        for l in range(0,total):
            df.loc[index]=["Easyship",data['rates'][l]['courier_name'],"20*10*10",weight,"HK",shortcode[testlist[k]],data['rates'][l]['total_charge'],d1,data['rates'][l]['max_delivery_time'],data['rates'][l]['min_delivery_time'],data['rates'][l]['available_handover_options']]
            index=index+1
    else:
        print('error')
        error_number=error_number+1
        time.sleep( random.randint(10,19) )
        getdata(k,j,index,error_number)
    return index,error_number
    
def getdata2(k,j,index,error_number):# set destination country is HK weight 0-20kg
    jsontest["origin_country_id"]=countrycode[testlist[k]] 
    weight=j*0.5  
    jsontest["destination_country_id"]=96
    jsontest["items"][0]["actual_weight"]=weight
    r=callapi(jsontest)
    try :
        data=r.json()
        print('success')
    except :
        time.sleep( random.randint(10,29) ) 
        print("not Json")  
        error_number=error_number+1 
        getdata(k,j,index,error_number)    
        
        
    if (r.status_code==200) & ('rates'in data):
        
        total=len(data['rates'])
        for l in range(0,total):
            df.loc[index]=["Easyship",data['rates'][l]['courier_name'],"20*10*10",weight,"HK",shortcode[testlist[k]],data['rates'][l]['total_charge'],d1,data['rates'][l]['max_delivery_time'],data['rates'][l]['min_delivery_time'],data['rates'][l]['available_handover_options']]
            index=index+1
    else:
        print('error')
        error_number=error_number+1
        time.sleep( random.randint(10,19) )
        getdata(k,j,index,error_number)
    return index,error_number 

def getdata3(k,j,index,error_number):# set origin country is HK weight 30-300kg
    jsontest["origin_country_id"]=96  
    weight=30+j*10
    jsontest["destination_country_id"]=countrycode[testlist[k]]
    jsontest["items"][0]["actual_weight"]=weight
    r=callapi(jsontest)
    try :
        data=r.json()
        print('success')
    except :
        time.sleep( random.randint(10,29) ) 
        print("not Json")  
        error_number=error_number+1 
        getdata(k,j,index,error_number)    
        
        
    if (r.status_code==200) & ('rates'in data):
        
        total=len(data['rates'])
        for l in range(0,total):
            df.loc[index]=["Easyship",data['rates'][l]['courier_name'],"20*10*10",weight,"HK",shortcode[testlist[k]],data['rates'][l]['total_charge'],d1,data['rates'][l]['max_delivery_time'],data['rates'][l]['min_delivery_time'],data['rates'][l]['available_handover_options']]
            index=index+1
    else:
        print('error')
        error_number=error_number+1
        time.sleep( random.randint(10,19) )
        getdata(k,j,index,error_number)
    return index,error_number
    

def getdata4(k,j,index,error_number):# set destination country is HK weight 30-300kg
    jsontest["origin_country_id"]=countrycode[testlist[k]] 
    weight=30+j*10  
    jsontest["destination_country_id"]=96
    jsontest["items"][0]["actual_weight"]=weight
    r=callapi(jsontest)
    try :
        data=r.json()
        print('success')
    except :
        time.sleep( random.randint(10,29) ) 
        print("not Json")  
        error_number=error_number+1 
        getdata(k,j,index,error_number)    
        
        
    if (r.status_code==200) & ('rates'in data):
        
        total=len(data['rates'])
        for l in range(0,total):
            df.loc[index]=["Easyship",data['rates'][l]['courier_name'],"20*10*10",weight,"HK",shortcode[testlist[k]],data['rates'][l]['total_charge'],d1,data['rates'][l]['max_delivery_time'],data['rates'][l]['min_delivery_time'],data['rates'][l]['available_handover_options']]
            index=index+1
    else:
        print('error')
        error_number=error_number+1
        time.sleep( random.randint(10,19) )
        getdata(k,j,index,error_number)
    return index,error_number 


def callapi(json):
    time.sleep( random.randint(10,19) )
    jsontest=json
    r=requests.post(url=url,headers=headers,json=jsontest)
    return r    

for k in range(0,12):
    for j in range(1,41):
        print("1-",k,"-",j)
        try:
            index,error_number=getdata(k,j,index,error_number)
            logging.info("right now it finished 1- %d - %d ",k,j)
        except Exception:
            logging.info(Exception)
for k in range(0,12):
    for j in range(1,41):
        print("2-","-",j)
        try:
            index,error_number=getdata2(k,j,index,error_number)
            logging.info("right now it finished 2- %d - %d ",k,j)
        except Exception:
            logging.info(Exception)
for k in range(0,12):
    for j in range(0,28):
        print("3-",k,"-",j)
        try:
            index,error_number=getdata3(k,j,index,error_number)
            logging.info("right now it finished 3- %d - %d ",k,j)
        except Exception:
            logging.info(Exception)
for k in range(0,12):
    for j in range(0,28):
        print("4-",k,"-",j)
        try:
            index,error_number=getdata4(k,j,index,error_number)
            logging.info("right now it finished 4- %d - %d ",k,j)
        except Exception:
            logging.info(Exception)

df["dropoff"]=df["available_handover_options"].str.contains("dropoff")
df["free_pickup"]=df["available_handover_options"].str.contains("free_pickup")
df["paid_pickup"]=df["available_handover_options"].str.contains("paid_pickup")
df['pickup_service']=df["free_pickup"] | df["paid_pickup"]
df_final=df.drop(columns=['available_handover_options'])
#df_final.to_csv("C:/Users/Luffy Zhang/Desktop/easyshiptest_2021.12.6.csv",index=False)

outdir = '../data/'
filename = 'easyship_Report' + thisdate + '.csv'
#df1.to_csv("C:/Users/Luffy Zhang/Desktop/spaceshiptestv1.4_2021.11.18.csv",index=False) 
df_final.to_csv(os.path.join(outdir, filename), index=False)  





