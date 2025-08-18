import torch
import gc

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