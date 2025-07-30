import json
import torch
import gc
from transformers import AutoTokenizer, AutoModelForCausalLM

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