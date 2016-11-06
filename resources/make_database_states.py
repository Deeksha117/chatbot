import pymongo

client = pymongo.MongoClient()


db = client.traveldata

"""dct = {"name":"Tamil Nadu", "pincode":"234561"}
db.states.insert(dct);

dct = {"name":"Lakshdweep", "pincode":"451251"}
db.states.insert(dct);"""

#printing from traveldata.states table
count = 0
for post in db.states.find({}):
	print count
	count += 1
	print post["name"]
	print post["pincode"]

#Deleting a database ------------- client.drop_database("mydb")
#removing entry from database

db.states.remove({"name":"Lakshdweep"})
