from pymongo import MongoClient


client = MongoClient("mongodb://localhost:27017")
db = client['Chicago_Car_Accidents']

accidents = db['accidents']
injuries = db['injuries']

