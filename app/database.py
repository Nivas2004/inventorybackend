from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL")  # Load it from .env

if not MONGO_URL:
    print("❌ MongoDB URL NOT LOADED. Check your .env file!")
else:
    print("🟢 MongoDB URL Loaded From .env")

client = AsyncIOMotorClient(MONGO_URL)
db = client.inventory_db
products_collection = db.get_collection("products")
users_collection = db.get_collection("users")


print("DEBUG MONGO_URL:", MONGO_URL)
