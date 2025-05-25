import os
from pymongo import MongoClient


MONGO_URL = os.environ.get("MONGO_URL")


client = MongoClient(MONGO_URL)
db = client["memorias"]
recipes_collection = db["receitas"]
user_collection = db["usuarios"]
