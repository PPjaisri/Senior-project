import json
from pymongo import MongoClient 
  
  
# Making Connection
myclient = MongoClient("mongodb+srv://lion:dulyawat@senior-project.agl3o.mongodb.net/test?authSource=admin&replicaSet=atlas-ofhdrm-shard-0&readPreference=primary&appname=MongoDB%20Compass&ssl=true") 
   
# database 
db = myclient["JSON_News"]
   
# Created or Switched to collection 
# names: GeeksForGeeks
Collection = db["ImportTest"]
  
# Loading or Opening the json file
with open('news_text.json',encoding="utf8") as file:
    file_data = json.load(file)
      
# Inserting the loaded data in the Collection
# if JSON contains data more than one entry
# insert_many is used else inser_one is used
if isinstance(file_data, list):
    Collection.insert_many(file_data)  
else:
    Collection.insert_one(file_data)