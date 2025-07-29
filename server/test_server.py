import json
import os
import torch
import gc
from transformers import AutoTokenizer, AutoModelForCausalLM
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"


import time
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

client = MongoClient("mongodb://localhost:27017")
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
                "updated_at": datetime.utcnow()
            }
        }
    )

def load_models_config(path="server/models.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_model_by_id(models, model_id):
    for model in models:
        if model["id"] == model_id:
            return model
    raise ValueError(f"Couldn't find model with id: {model_id}")

def load_model_and_tokenizer(model_path, trust_remote_code=False):
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=trust_remote_code)
    model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=trust_remote_code)
    return tokenizer, model

def prompt_qwen(tokenizer, model, user_input):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.eval()

    prompt = f"<|user|>\n{user_input}\n<|assistant|>"
    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    outputs = model.generate(
        **inputs,
        max_new_tokens=512,
        do_sample=False
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=False)
    return response

def prompt_llama(tokenizer, model, user_input):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model = model.to(device)
    model.eval()

    prompt = f"[INST] {user_input} [/INST]"
    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = {k: v.to(device) for k, v in inputs.items()}

    outputs = model.generate(
        **inputs,
        max_new_tokens=512,
        do_sample=False
    )

    response = tokenizer.decode(outputs[0], skip_special_tokens=False)
    return response

def clear_memory(model=None, tokenizer=None):
    try:
        if model:
            model.cpu()
            del model
        if tokenizer:
            del tokenizer
    except Exception as e:
        print(f"Memory clean error")
    finally:
        gc.collect()
        if torch.cuda.is_available():
            with torch.cuda.device(torch.cuda.current_device()):
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()

def select_model(models):
    for model in models:
        print(f"[{model['id']}] {model['name']} ({model['type']})")
    selected_id = int(input("Model ID: "))
    model_info = get_model_by_id(models, selected_id)
    if not os.path.exists(model_info["path"]):
        raise FileNotFoundError(f"Path doesn't exists: {model_info['path']}")
    trust_remote = model_info.get("trust_remote_code", False)
    tokenizer, model = load_model_and_tokenizer(model_info["path"], trust_remote)
    print(f"Loaded: {model_info['name']} ({model_info['type']})")
    return model_info, tokenizer, model

def main():
    models = load_models_config()
    model_info, tokenizer, model = None, None, None
    current_model_id = None

    try:
        print("Server listening...")
        while True:
            task = fetch_pending_prompt()
            if task:
                prompt = task["prompt"]
                model_id = task.get("model_id", 1)
                doc_id = task["_id"]
                print(f"📥 Prompt (model {model_id}): {prompt}")

                if model_id != current_model_id:
                    print("Changing model")
                    clear_memory(model, tokenizer)
                    model_info = get_model_by_id(models, model_id)
                    tokenizer, model = load_model_and_tokenizer(model_info["path"])
                    current_model_id = model_id

                if model_info["type"] == "qwen":
                    response = prompt_qwen(tokenizer, model, prompt)
                elif model_info["type"] == "llama":
                    response = prompt_llama(tokenizer, model, prompt)
                else:
                    response = "model err"

                update_response(doc_id, response)
                print("Answer send\n")

            time.sleep(2)
    finally:
        clear_memory(model, tokenizer)
        print("memory cleaned")

if __name__ == "__main__":
    main()
