#!/usr/bin/python

#USING MONGOdb, for python
import pymongo

#creating a new user session
client = pymongo.MongoClient()

#creating a new DB called, traveldata
db = client.traveldata

try:
	db.destinations.drop()
except:
	pass
import parse_state
import parse_city
import insert_popular_places
