#!/usr/bin/python

#USING MONGOdb, for python
import pymongo

#creating a new user session
client = pymongo.MongoClient()

#creating a new DB called, traveldata
db = client.traveldata
import requests
from lxml import html

## Open the file to read all states
f = open("0", "r")
states = f.readlines()
f.close()

#print states

states_DS=[]
state_data={}

#only storing user-reviews, for sentiment analysis
states_DS2=[]
state_data2={}

for x in range(0, 4):
    state_url = states[x]
    lst = state_url.split('/')
    st_name = lst[4]

    state_data['name']=st_name
    state_data['type']='state'
    state_data2['name']=st_name
    response = requests.get(state_url)
    tree = html.fromstring(response.text)

    #for state rating
    st_rating = tree.xpath("//div[starts-with(@class,'rating-container')]/@title")[0]
    state_data['ratings']=st_rating
    
    #for description
    l=[]
    l=tree.xpath('//div[@id="longDescriptionOne"]//span//p//span//text()')
    st_desc="".join(l)
    state_data['details']=st_desc

    #for vedio rating
    vedio=tree.xpath("//div[@class='footer-bottom-icon']//a/@href")[3]
    state_data['vedio_review']=vedio

    #for list of cities/destinations
    l=tree.xpath("//div[@class='about-photo']//h5//a//text()")
    temp=[]
    for place in l:
	l2=place.split(',')
        temp.append(l2[0])
    state_data['places']=temp

    #for list of cities/destinations ---- user reviews
    l=tree.xpath("//div[@class='review-block ']//blockquote//text()")
    state_data['reviews']=l
    state_data2['reviews']=l
    
    #print state_data
    #INSERTING one state's data as a dictionary record in DB
    db.states.insert(state_data.copy());
    states_DS.append(state_data)
    states_DS2.append(state_data2)
#print states_DS

#printing from traveldata.states table
count = 0
for post in db.states.find({}):
	print count
	count += 1
	print post["name"]
	print post["ratings"]
        print post["details"]
        print post["places"]
	print post["vedio_review"]
	print post["reviews"]
    


