#!/usr/bin/python
from api_ai_request import api_request as api_request
import pymongo

client = pymongo.MongoClient()
db = client.traveldata

#print response

class Response_Functions:
    def __init__(self):
    	self.data = []

    def get_description(self,ids):
    	#print ids
    	print str(db.states.find({"name":ids.lower()})[0]["description"])
    def get_destination(self,ids):
    	print str(db.states.find({"name":ids.lower()})[0]["places"])



while(1):
	user_query = []
	query = raw_input("User : ")
	user_query.append(query.split("."))  #if query is seperated by full stop. send as 'n' diffrent queries to api.ai
	response = api_request(user_query)
	
	if response["status"]["code"]!=200:
		print "Sorry. Server cannot be contacted."
		exit

	obj = Response_Functions()
	#if response["intentName"]=="description":
	key1=response["result"]["parameters"]["name"].lower()
	key2=response["result"]["parameters"]["name1"].lower()

	if response["result"]["action"]=="get_description":
		if key1:
			obj.get_description(key1)
		elif key2:
			obj.get_description(key2)
		else :
			print "Sorry we have'nt got any response for you"

	elif response["result"]["action"]=="get_destination":
		if key1:
			obj.get_destination(key1)
		elif key2:
			obj.get_destination(key2)
		else :
			print "Sorry we have'nt got any response for you"



