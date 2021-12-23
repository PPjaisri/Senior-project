from flask import Flask
from flask_pymongo import pymongo
from app import app
CONNECTION_STRING = "mongodb+srv://lion:tigerlion007@cluster0.uojms.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = pymongo.MongoClient(CONNECTION_STRING)
db = client.get_database('Helloworld')
user_collection = pymongo.collection.Collection(db, 'TestUserInput')