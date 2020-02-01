import requests, json
import pandas as pd
import urllib3 as urllib
import numpy as np
import pprint
import re, datetime
from datetime import date
def operations(r):
    dist=r.json()
    dist_=dist['links']
    description=dist['descriptions']
    resized=dist['resized_images']
    pprint.PrettyPrinter(indent=1).pprint(dist)
    
    
    length=np.size(description)
    
    month_list_full=["january","february","march","april","may","june","july","august","september","october","november","december"]
    month_list_short=["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
    
    for i in range(length):
        string=str.lower(description[i])
        for K in range(4):
            for j in range(12):
                month_short=month_list_short[j]
                month_full=month_list_full[j]
                string=string.replace(month_full,month_short)
        description[i]=string
        
        
    
    #Searching of Pattern of type for exmaple nov 12 2019 
    date_=[]
    for i in range(length):
        s=description[i]
        match = re.search('\w{3}\s\d{2},\s\d{4}', s)
        if(match is None):
            continue
        k=str.lower(match[0])
        date_=np.append(date_,k)
    
    length=np.size(date_)
    #creating Data frame form json file which contain Date 
    #Extracting of Month
    month_=[]
    for i in range(length):
        month=[{'jan':1,'feb':2,'mar':3,'apr':4,'may':5,'jun':6,'jul':7,'aug':8,'sep':9,'oct':10,'nov':11,'dec':12}]#,"january":1,"february":2,"march":3,"april":4,"may":5,"june":6,"july":7,"august":8,"september":9,"october":10,"november":11,"december":12}]
        k=date_[i][0:3]
        month_value=int(month[0][k])
        month_=np.append(month_,month_value)
    
    data_news=pd.DataFrame(data=month_,columns=['Month'],dtype=np.int8)
    
    #Extracting of Day
    day=[]
    for j in range(length):
        k=date_[j][4:6]
        day=np.append(day,k)
    
    data_news['day']=pd.DataFrame(data=day,dtype=np.int8)
    
    #Extracting Of Year
    year=[]
    for j in range(length):
        k=date_[j][8:12]
        year=np.append(year,k)
        
    data_news['year']=pd.DataFrame(data=year,dtype=int)   
    
    #Present date
    from datetime import date
    today = date.today()
    cur_month=today.month
    cur_day=today.day
    cur_year=today.year
    
    
    #finding when does first news appear
    array=data_news.year
    array=array*1000
    array=array+data_news.Month*100
    array=array+data_news.day
    index=np.argmax(array)
    latest_date=data_news.values[1]
    
    cur_date=[cur_year,cur_day,cur_day]
    #FInding GAP
    Start=date(latest_date[2],latest_date[0],latest_date[1])
    End=date(cur_year,cur_month,cur_day)
    Gap=(End-Start).days
    yyyy=Gap//365
    mm=(Gap%365)//30
    dd=((Gap%365)%30)
    diff=[mm,dd,yyyy]
    
    #printing Difference
    
    if(diff[0]==0 and diff[1]==0 and diff[2]==0):
        print("Todays News")
    
    else:
        print("News is of",end=" ")
        if(diff[1]!=0):
            print("{} days".format(diff[1]),end=" ")
        if(diff[0]!=0):
            print("{} Month".format(diff[0]),end=" ")
        if(diff[2]!=0):
            print("{} Year".format(diff[2]),end=" ")
        print("older\nThank You")
    
    
        
