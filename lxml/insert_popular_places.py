#!/usr/bin/python

#USING MONGOdb, for python
import pymongo

#creating a new user session
client = pymongo.MongoClient()

#creating a new DB called, traveldata
db = client.traveldata

## Open the file to read all places
f = open("../resources/Popularplaces.txt", "r")
lines = f.readlines()
f.close()

state_data={}
flag=0
temp=[]
for oneline in lines:
    if oneline[0] == "#":
        if len(temp) > 0:
            state_data['places']=temp 
            db.destinations.insert(state_data.copy())
        st_name = oneline[1:-1]
        state_data['name']=st_name.lower()
        state_data['type']='common'
	temp=[]
    else:
        temp.append(oneline[:-1])

if len(temp) > 0:
    state_data['places']=temp 
    db.destinations.insert(state_data.copy())

count = 0
for post in db.destinations.find({'type':'common'}):
    print count
    count += 1
    print post["name"]
    print post["type"]
    print post["places"]


## Open the file to read all places
f = open("../resources/Popularplaces2.txt", "r")
lines = f.readlines()
f.close()

city_data={}
flag=0
temp=[]
for oneline in lines:
    if oneline[0] == "#":
        if len(temp) > 0:
            city_data['places']=temp 
            db.destinations.remove({"name":city_name.lower()})
            db.destinations.insert(city_data.copy())
        city_name = oneline[1:-1]
        city_data=db.destinations.find({"name":city_name.lower()})[0]
	temp=[]
    else:
        temp.append(oneline[:-1])

if len(temp) > 0:
    city_data['places']=temp 
    db.destinations.remove({"name":city_name.lower()})
    db.destinations.insert(city_data.copy())





    
    

