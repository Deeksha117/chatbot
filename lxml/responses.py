#!/usr/bin/python
from api_ai_request import api_request as api_request
import pymongo
import datetime
from random import randint
import socket
client = pymongo.MongoClient()
db = client.traveldata
now = datetime.datetime.now()
"""class Response_Functions:
    member-variables : self, data=[]
    member-functions : get_description,get_destination, get_review, ...
    one function againsta each intent. Fetches result from database, and formulates response
"""
def text_processing(strn):
    return ", ".join(strn.split('.')[:4])


class Response_Functions:
    def __init__(self):
        self.data = []

    #Function called when intent is description
    def get_description(self,ids):
        #print ids
        counter=(randint(0,3))
        res_list=["Hola!\n Let me guide your Travel,\n\n", "Well,\n\n", "Let me give you some details,\n\n", "Your Travel guide says,\n\n"]
        try:
            record=db.destinations.find({"name":ids.lower()})[0]
        except:
            return "No description available for this place."

        if record["type"] == 'state':
            return res_list[counter]+text_processing(record["details"])
            #keyword extraction

        elif record["type"] == 'city':
            strn = record["details"]
            #strn = strn+str(ids)+" is located in the state of "+record["city_statename"]
            strn = strn+ ". Best time to visit is " + " ".join(record["city_bestTime"])
            #record["famousfor"]
            return res_list[counter]+strn
        elif record["type"] == "common":
        	return self.get_destination(ids)
        else:
            return "Please be more specific."
        #return res_list[counter]+"".join(db.destinations.find({"name":ids.lower()})[0]["details"].split('.')[:4])

    #function called when intent is destination
    def get_destination(self,ids):
    	print ids
        #themes = ['beach', 'hill', 'adventure', 'jungle', 'honeymoon', 'desert', 'waterfront' ]
        try:
            record=db.destinations.find({"name":ids.lower()})[0]
        except:
            return "No destinations available for this place."
        places = record["places"]

        if record["type"] == "common":
            strn = "You can choose among these popular "+ids+" places : "

        #call db for popular places and return
        # else for proper nouns: states and cities, fetch from db
        elif record["type"] == "state":
            strn = ids + " has the following popular cities to visit:\n"
        else: 
            strn = "Popular Sightseeing places in "+ids+" are:\n"
        strn = strn + "\n"
        for p in places:
            strn=strn+str(p).title()+", "
        return strn

    #function called when intent is rating
    def get_rating(self,ids):
        try:
            record=db.destinations.find({"name":ids.lower()})[0]
        except:
            return "Rating not available for this place."
        counter=(randint(0,3))
        res_list=["According to Traveller feedback,\n", "Suggested by Travellers,\n", "Several Travellers have given,\n", "Travellers say,\n"]
        try:
            strn= res_list[counter]+record["ratings"] + ", for " +ids.title()+"\nYou may also like to see this video review from a traveller,\n" + record["video_review"]
        except:
            strn = "Please be more specific."
        return strn


    #function called when intent is review
    def get_review(self,ids):
        try:
            record=db.destinations.find({"name":ids.lower()})[0]
        except:
            return "No review available for this place."
        try:
            strn = "Dear Traveller "+ ids.title()+" Reviews are as follows,\n"
            strn = strn + ">> " +str(record["reviews"][0])
            strn = strn + "\n\n>> " +str(record["reviews"][1])
        except:
            strn = "Please be more specific."
        return strn

    def get_how_to_reach(self,ids,transport):
    	#print "how to reach",ids
    	try:
            record=db.destinations.find({"name":ids.lower()})[0]
        except:
            return "Sorry we could not get you. Can you be more specific."

    	if(transport==""):
    		#give default reply
            strn = "You can travel via Bus, Train, Flight or Cab. How would you prefer to go?"
    		
    	else:
            strn = record["mode"][transport]
    		#give record["mode"][transport]
        
        return strn

    def best_time(self,ids):
        try:
            record=db.destinations.find({"name":ids.lower()})[0]
        except:
            return "Sorry we could not get you. Can you be more specific."
        
        if record["type"]=="city":
            strn = "Best time to visit "+ids+" is " + " ".join(record["city_bestTime"])
        else:
            strn = "Please specify city name!"

        return strn

    def make_plan(self,ids,month,duration):
    	#print "make_plan",ids,month,duration
        try:
            record=db.destinations.find({"name":ids.lower()})[0]
        except:
            return "No plan available for this place."

        if record["type"]=="city":
            if duration<"3" :
                #local sightseeing
                places=record["places"]
                pass
            else:
                #nearby ciies of same state
                state = record["city_statename"]
                try:
                    record_state = db.destinations.find({"name":state.lower()})[0]
                except:
                    return "Sorry. I am unable to plan your travel."
                strn = "For local sightseeing you can visit: "
                #print record
                places = record["places"][:4]
                strn = strn + "\n"
                for p in places:
                        strn=strn+str(p).title()+", "
                #print record_state
                record_state["places"][:4]
        elif record["type"]=="state":
            places = record["places"][:3]

        else:                                           #for record["type"]='common'
            places = record["places"]

        strn = "You can visit the following places "
        strn = strn + "\n"
        for p in places:
                strn=strn+str(p)+", "
        return strn



"""query_handler
I/P : query from user_query
O/P : response from chatbot"""
def query_handling(query):
    user_query = []
    user_query.append(query.split("."))             #if query is seperated by full stop. send as 'n' diffrent queries to api.ai
    response = api_request(user_query)              #send query to api_ai and retrive a response dictionary

    if response["status"]["code"]!=200:
        return "Sorry. Server cannot be contacted."

    obj = Response_Functions()                      #object for receiving all responses from Response_Functions class
    
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
            #print "Sorry we have'nt got any response for you"
            return "Sorry we have'nt got any response for you"

    elif response["result"]["action"]=="get_review":
        if key1:
            return obj.get_review(key1)
        elif key2:
            return obj.get_review(key2)
        else :
            #print "Sorry we have'nt got any response for you"
            return "Sorry we have'nt got any response for you"

    elif response["result"]["action"]=="get_how_to_reach":
    	try:
    		transport = response["result"]["parameters"]["transport"].lower()
    	except:
    		transport = ""
        if key1:
            return obj.get_how_to_reach(key1,transport)
        elif key2:
            return obj.get_how_to_reach(key2,transport)
        else :
            return "Sorry we have'nt got any response for you"

    elif response["result"]["action"]=="best_time":
        if key1:
            return obj.best_time(key1)
        elif key2:
            return obj.best_time(key2)
        else :
            return "Sorry we have'nt got any response for you"

    elif response["result"]["action"]=="make_plan":
    	try:
    		duration = response["result"]["parameters"]["duration"]
    	except:
    		duration = "5"
    	try:
    		month = response["result"]["parameters"]["month"]
    	except:
    		month = now.month

        if key1:
            return obj.make_plan(key1,month,duration)
        elif key2:
            return obj.make_plan(key2,month,duration)
        else :
            return "Sorry we have'nt got any response for you"

    else:
        return "Sorry we have'nt got any response for you. Please enter some other query."
    #elif response["result"]["action"]=="smalltalk.greetings":
        #print response["result"]["fulfillment"]["speech"]
    #   return response["result"]["fulfillment"]["speech"]



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
            #try:
            resp = (query_handling(buf))
            #except:
            # resp = resp.encode('ascii')
            #resp = resp.encode('ascii', 'ignore')
            print "TRIPPO: ",resp

    

    
