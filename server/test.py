import json
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch


def load_models_config(path="server/models.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_model_by_id(models, model_id):
    for model in models:
        if model["id"] == model_id:
            return model
    raise ValueError(f"Couldn't find model with id: {model_id}")


def load_model_and_tokenizer(model_path):
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=False)
    model = AutoModelForCausalLM.from_pretrained(model_path, trust_remote_code=False)
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

def main(model_id, user_input):
    models = load_models_config()
    model_info = get_model_by_id(models, model_id)

    if not os.path.exists(model_info["path"]):
        raise FileNotFoundError(f"Couldn't find model with path: {model_info['path']}")

    tokenizer, model = load_model_and_tokenizer(model_info["path"])

    if model_info["type"] == "qwen":
        response = prompt_qwen(tokenizer, model, user_input)
    elif model_info["type"] == "llama":
        response = prompt_llama(tokenizer, model, user_input)
    else:
        raise ValueError(f"Could not find model type: {model_info['type']}")
    print(response)


if __name__ == "__main__":
    selected_model_id = 1

    user_prompt = "Write function in python that returns modulo of two arguments."

    main(selected_model_id, user_prompt)
