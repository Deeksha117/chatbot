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
f = open("../urls_to_parse/1", "r")
city = f.readlines()
f.close()

#print states

city_DS=[]
city_data={}

#only storing user-reviews, for sentiment analysis
city_DS2=[]
city_data2={}

for x in range (0,10):
    city_url = city[x]
    lst = city_url.split('/')
    city_name=lst[4]

    city_data['name'] = city_name.lower()
    city_data['type'] = 'city'
    city_data2['name'] = city_name.lower()
    response = requests.get(city_url)
    tree = html.fromstring(response.text)

    #for city rating
    city_rating = tree.xpath("//div[starts-with(@class,'rating-container')]/@title")[0]
    city_data['ratings']=city_rating

    #Famous for
    #city_famous = tree.xpath("//div[@class='button-category dest-sprite destination-detail-heritage']//text()")
    #print city_famous
    #city_data['Famous_for'] = city_famous.lower()

    #Travel Guide
    city_guide = tree.xpath("//div[@class='pdf-link-Section']//a/@href")[0]
    city_data['travel_guide'] = city_guide
    
    #rank
    temp1=tree.xpath('//div[@class="rank-bar"]//span//text()')[1]
    temp2=temp1.split()
    city_rank=temp2[0]+' '+temp2[1]+' '+temp2[2]+' '+temp2[3]
    city_data['city_rank'] = city_rank

    #State name
    city_statename = tree.xpath('//div[@id="aboutDestination"]//ul//li//text()')[1]
    city_data['city_statename'] = city_statename


    #Best Time
    city_bestTime = tree.xpath("//div[@class='upcoming alignleft']//ul//li[@class='bestTime']//text()")
    city_data['city_bestTime'] = city_bestTime

    #user reviews
    city_reviews = tree.xpath("//div[@class='review-block ']//blockquote//text()")
    city_data['city_reviews'] = city_reviews

    #Things to do in city(pending)
    #l=tree.xpath('//div[@id="longDescription11"]//p//text()')
    #print state_data
    #Inserting one city's data as a dictionary record in DB

    db.destinations.insert(city_data.copy());
    city_DS.append(city_data)

    #print city_DS
    #printing from traveldata.destinations table

count = 0
for post in db.destinations.find({"type":"city"}):
	print count
	count += 1
	print post["name"]
	print post["type"]
	print post["ratings"]
	#print post["Famous_for"]
	print post["travel_guide"]
	print post["city_rank"]
	print post["city_statename"]
	print post["city_bestTime"]
	print post["city_reviews"]



    
