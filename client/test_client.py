import requests
import time
import uuid

from dotenv import load_dotenv
import os

load_dotenv()

def send_prompt(prompt, model_id):
    doc_id = str(uuid.uuid4())

    payload = {
        "id": doc_id,
        "prompt": prompt,
        "model": model_id
    }

    try:
        response = requests.post(f"{os.getenv("API_URL")}/request", json=payload)
        response.raise_for_status()
        return doc_id
    except Exception as e:
        print("Failed to send prompt:", e)
        exit(1)

def ask_for_models():
    try:
        response = requests.get(f"{os.getenv("API_URL")}/models")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Connection failed:", e)
        exit(1)


if __name__ == "__main__":
    [print(f"[{model[0]}]. {model[1]}") for model in ask_for_models()]

    model_id = input("Model id: ")
    prompt = input("Prompt: ")

    doc_id = send_prompt(prompt, model_id)
