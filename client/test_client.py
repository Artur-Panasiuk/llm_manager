import time
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb://localhost:27017")
db = client.chat_db
collection = db.prompts

def send_prompt(prompt_text, model_id):
    doc = {
        "prompt": prompt_text,
        "model_id": model_id,
        "response": None,
        "status": "pending",
    }
    result = collection.insert_one(doc)
    return result.inserted_id

def wait_for_response(doc_id, timeout=360):
    start = time.time()
    while time.time() - start < timeout:
        doc = collection.find_one({"_id": ObjectId(doc_id)})
        if doc and doc.get("status") == "done":
            return doc["response"]
        time.sleep(1)
    return None

if __name__ == "__main__":
    prompt = input("Prompt: ")

    print("Model:")
    print("  0 - Qwen")
    print("  1 - LLaMA")
    try:
        model_id = int(input("Model ID: ").strip())
    except ValueError:
        exit(1)

    doc_id = send_prompt(prompt, model_id)
    print("Waiting")
    response = wait_for_response(doc_id)

    if response:
        print("\nANS:\n", response)
    else:
        print("\nTIMEOUT\n")
