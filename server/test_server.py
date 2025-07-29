import json
import os
import torch
import gc
from transformers import AutoTokenizer, AutoModelForCausalLM
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

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

    model_info, tokenizer, model = select_model(models)

    try:
        while True:
            user_input = input("> ").strip()
            if user_input.lower() in ["exit", "quit"]:
                break
            elif user_input.lower() in ["!switch"]:
                clear_memory(model, tokenizer)
                model_info, tokenizer, model = select_model(models)
                continue

            if model_info["type"] == "qwen":
                response = prompt_qwen(tokenizer, model, user_input)
            elif model_info["type"] == "llama":
                response = prompt_llama(tokenizer, model, user_input)
            else:
                continue

            print(response)
    finally:
        clear_memory(model, tokenizer)

if __name__ == "__main__":
    main()
