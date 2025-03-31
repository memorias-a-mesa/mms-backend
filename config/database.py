from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb+srv://isabellescarso:isabelle@cluster0.xqtwo.mongodb.net/"
client = AsyncIOMotorClient(MONGO_URI)
db = client["memorias-a-mesa"]
recipes_collection = db["receitas"]