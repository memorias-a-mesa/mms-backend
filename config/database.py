from motor.motor_asyncio import AsyncIOMotorClient
import os


MONGO_URL = os.environ.get("MONGO_URL")


client = AsyncIOMotorClient(MONGO_URL, tls=True, tlsAllowInvalidCertificates=True)
db = client["memorias-a-mesa"]
recipes_collection = db["receitas"]
user_collection = db["usuarios"]
