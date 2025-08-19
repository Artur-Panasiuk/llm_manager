from dotenv import load_dotenv
import requests
import uuid
import time
import os

load_dotenv()

def send_prompt(prompt, model_id, tokens):
    doc_id = str(uuid.uuid4())

    payload = {
        "task_id": doc_id,
        "model_name": model_id,
        "prompt": prompt,
        "tokens": tokens
    }

    try:
        response = requests.post(f"http://{os.getenv("NETWORK_IP")}:{os.getenv("NETWORK_PORT")}/request", json=payload)
        response.raise_for_status()
        return doc_id
    except Exception as e:
        print("Failed to send prompt:", e)
        exit(1)

def ask_for_models():
    try:
        response = requests.get(f"http://{os.getenv("NETWORK_IP")}:{os.getenv("NETWORK_PORT")}/models")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Connection failed:", e)
        exit(1)

def ask_for_answer(doc_id):
    try:
        response = requests.get(f"http://{os.getenv("NETWORK_IP")}:{os.getenv("NETWORK_PORT")}/get/{doc_id}")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print("Connection failed:", e)
        exit(1)

if __name__ == "__main__":
    [print(f"{model}") for model in ask_for_models()]

    model_name = input("Model name: ")
    prompt = input("Prompt: ")
    tokens = input("Tokens: ")

    doc_id = send_prompt(prompt, model_name, tokens)

    timeout = 999
    poll_interval = 2
    waited = 0
    result = None

    while waited < timeout:
        answer = ask_for_answer(doc_id)
        
        if answer.get("status") == "done":
            result = answer.get("result", "")
            break

        time.sleep(poll_interval)
        waited += poll_interval

    if result:
        print("AI response:", result)
    else:
        print("Timeout reached. No response from server.")