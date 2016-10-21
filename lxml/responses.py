#!/usr/bin/python
from api_ai_request import api_request as api_request
import pymongo

client = pymongo.MongoClient()
db = client.traveldata

"""class Response_Functions:
	member-variables : self, data=[]
	member-functions : get_description,get_destination, get_review, ...
	one function againsta each intent. Fetches result from database, and formulates response
"""
class Response_Functions:
    def __init__(self):
    	self.data = []

    #Function called when intent is description
    def get_description(self,ids):
    	#print ids
    	print str(db.states.find({"name":ids.lower()})[0]["description"])

    #function called when intent is destination
    def get_destination(self,ids):
    	print str(db.states.find({"name":ids.lower()})[0]["places"])


#main body
while(1):
	user_query = []
	query = raw_input("User : ")			#take query input from user
	user_query.append(query.split(".")) 	#if query is seperated by full stop. send as 'n' diffrent queries to api.ai
	response = api_request(user_query)		#send query to api_ai and retrive a response dictionary

	if response["status"]["code"]!=200:
		print "Sorry. Server cannot be contacted."
		exit

	obj = Response_Functions()
	
	key1=response["result"]["parameters"]["place_name"].lower()
	key2=response["result"]["parameters"]["place_context"].lower()

	#Matching action name with function call from Response_Functions call
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



