#!/usr/bin/python

#USING MONGOdb, for python
import pymongo

#creating a new user session
client = pymongo.MongoClient()

#creating a new DB called, traveldata
db = client.traveldata

import requests
from lxml import html

## Open the file to read all places
f = open("../urls_to_parse/4", "r")
cities = f.readlines()
f.close()

#print states
city_DS=[]
city_data={}
print cities
for x in range(0, len(cities)):
    city_url = cities[x]
    lst = city_url.split('/')
    city_name = lst[4].split('-')[0]
    
    #city_data['name']=city_name.lower()
    city_data=db.destinations.find({"name":city_name.lower()})[0]
    print city_name.lower()
    print type(city_data)

    mode_dict = {}
    response = requests.get(city_url)
    tree = html.fromstring(response.text)

    #for train
    mode = tree.xpath("//div[@class='quick-links-destination']//p//text()")
    #print mode
    #print "\n\n\n\n\n"
    for zz in range(0,len(mode)):
        if mode[zz].find("Bus")!=-1 and mode[zz].find("By")!=-1:
	        b=zz
    	if mode[zz].find("Train")!=-1 and mode[zz].find("By")!=-1:
    	    t=zz
    	if mode[zz].find("Flight")!=-1 and mode[zz].find("By")!=-1:
    	    f=zz
    	if mode[zz].find("Car")!=-1 and mode[zz].find("By")!=-1:
    	    c=zz

    desc=""
    #print b,mode[b]
    for x in range(0, b):
    	desc=desc+mode[x].strip()
    print desc
    city_data["details"]=desc

    temp=""
    for x in range(b, t-1):
    	temp=temp + mode[x].strip()
    mode_dict['bus'] = temp
    #print "\n" + temp

   

    temp=""
    for x in range(t, f-1):
    	temp=temp + mode[x].strip()
    mode_dict['train'] = temp
    #print "\n"+ temp

    temp=""
    for x in range(f, c-1):
    	temp=temp + mode[x].strip()
    mode_dict['flight'] = temp
    #print "\n"+temp

    temp=""
    for x in range(c, len(mode)):
    	temp=temp + mode[x].strip()
    mode_dict['cab'] = temp
    #print "\n"+temp
   
    city_data['mode'] = mode_dict

    #INSERTING one city reach data as a dictionary record in DB
    db.destinations.remove({"name":city_name.lower()})
    db.destinations.insert(city_data.copy())

#printing from traveldata.destinations table
count = 0
for post in db.destinations.find({'type':''}):
	print count
	count += 1
	print post["name"]
	print post["mode"]


