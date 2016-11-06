#!/usr/bin/python
from api_ai_request import api_request as api_request
import pymongo
from random import randint
import socket
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
		counter=(randint(0,3))
		res_list=["Hola!\n Let me guide your Travel,\n\n", "Well,\n\n", "Let me give you some details,\n\n", "Your Travel guide says,\n\n"]
		return res_list[counter]+"".join(db.destinations.find({"name":ids.lower()})[0]["details"].split('.')[:4])

    #function called when intent is destination
    def get_destination(self,ids):
    	themes = ['beach', 'hill', 'adventure', 'jungle', 'honeymoon', 'desert', 'waterfront' ]
    	for t in themes:
    		if t == ids:
    			print "beaches are: "
    			#call db for popular places and return
    	# else for proper nouns: states and cities, fetch from db
    	places = db.destinations.find({"name":ids.lower()})[0]["places"]
    	if db.destinations.find({"name":ids.lower()})[0]["type"] == "state":
    		strn = ids + " has the following popular places to visit:\n"
    	else : 
    		strn = "Popular Sightseeing places in "+ids+" are:\n"

    	strn = strn + "\n"
    	for p in places:
    		strn=strn+str(p)+", "
    	return strn

    #function called when intent is rating
    def get_rating(self,ids):
		counter=(randint(0,3))
		res_list=["According to Traveller feedback,\n", "Suggested by Travellers,\n", "Several Travellers have given,\n", "Travellers say,\n"]
		return res_list[counter]+db.destinations.find({"name":ids.lower()})[0]["ratings"] + ", for " +ids.title()+"\nYou may also like to see this video review from a traveller,\n" + db.destinations.find({"name":ids.lower()})[0]["video_review"]

    #function called when intent is review
    def get_review(self,ids):
		strn = "Dear Traveller "+ ids.title()+" Reviews are as follows,\n"
		strn = strn + ">> " +str(db.destinations.find({"name":ids.lower()})[0]["reviews"][0])
		strn = strn + "\n\n>> " +str(db.destinations.find({"name":ids.lower()})[0]["reviews"][1])
		return strn


def query_handling(query):
	user_query = []
	#query = raw_input("User : ")			#take query input from user
	user_query.append(query.split(".")) 	        #if query is seperated by full stop. send as 'n' diffrent queries to api.ai
	response = api_request(user_query)		#send query to api_ai and retrive a response dictionary

	if response["status"]["code"]!=200:
		return "Sorry. Server cannot be contacted."
		#exit

	obj = Response_Functions()
	
	#if response["result"]["action"]!="smalltalk.greetings":
	try:
			key1=response["result"]["parameters"]["place_name"].lower()
			key2=response["result"]["parameters"]["place_namecontext"].lower()
	except:
			return response["result"]["fulfillment"]["speech"]

	#Matching action name with function call from Response_Functions call
	if response["result"]["action"]=="get_description":
		if key1:
			return obj.get_description(key1)
		elif key2:
			return obj.get_description(key2)
		else :
			#print "Sorry we have'nt got any response for you"
			return "Sorry we have'nt got any response for you"

	elif response["result"]["action"]=="get_destination":
		if key1:
			return obj.get_destination(key1)
		elif key2:
			return obj.get_destination(key2)
		else :
			#print "Sorry we have'nt got any response for you"
			return "Sorry we have'nt got any response for you"

	elif response["result"]["action"]=="get_rating":
		if key1:
			return obj.get_rating(key1)
		elif key2:
			return obj.get_rating(key2)
		else :
			print "Sorry we have'nt got any response for you"
			return "Sorry we have'nt got any response for you"

	elif response["result"]["action"]=="get_review":
		if key1:
			return obj.get_review(key1)
		elif key2:
			return obj.get_review(key2)
		else :
			#print "Sorry we have'nt got any response for you"
			return "Sorry we have'nt got any response for you"

	#elif response["result"]["action"]=="smalltalk.greetings":
		#print response["result"]["fulfillment"]["speech"]
	#	return response["result"]["fulfillment"]["speech"]



#main body
if __name__ == "__main__":
	choice = raw_input("1:for socket \t 2: for manual try\n")
	if choice=="1":
		serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		serversocket.bind(('localhost', 9988))
		serversocket.listen(5) # become a server socket, maximum 5 connections
		print "Chat server started on port " + str(9988)

		while True:
		    connection, address = serversocket.accept()
		    buf = connection.recv(256)
		    if len(buf) > 0:
		        print "USER: ",buf
		        resp=query_handling(buf)
		        print "TRIPPO: ",resp
		        connection.send(resp)
		    connection.close();
		serversocket.close()
	else:
		while(1):
			buf = raw_input("USER: ")
			#print "USER: ",buf
			resp = (query_handling(buf))
			# resp = resp.encode('ascii')
			#resp = resp.encode('ascii', 'ignore')
			print "TRIPPO: ",resp

    

	
