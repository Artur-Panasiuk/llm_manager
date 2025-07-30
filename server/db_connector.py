from dotenv import load_dotenv
import os
from pymongo import MongoClient
from bson.objectid import ObjectId

load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client.chat_db
collection = db.prompts

def fetch_pending_prompt():
    return collection.find_one({"status": "pending"})

def update_response(doc_id, response):
    collection.update_one(
        {"_id": ObjectId(doc_id)},
        {
            "$set": {
                "response": response,
                "status": "done",
            }
        }
    )