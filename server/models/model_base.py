import torch
import gc

class BaseModel:
    registry = {}

    def __init__(self):
        self.path = None
        self.model = None
        self.tokenizer = None

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseModel.registry[cls.__name__.lower()] = cls

    @classmethod
    def create(cls, name, *args, **kwargs):
        if name.lower() not in cls.registry:
            raise ValueError(f"Unknown model: {name}")
        return cls.registry[name.lower()](*args, **kwargs)
    
    @classmethod
    def available_models(cls):
        return list(cls.registry.keys())

    def clear_memory(self):
        try:
            if self.model:
                self.model.cpu()
                del self.model
            if self.tokenizer:
                del self.tokenizer
        except Exception as e:
            print(f"Memory clean error - {e}")
        finally:
            gc.collect()
            if torch.cuda.is_available():
                with torch.cuda.device(torch.cuda.current_device()):
                    torch.cuda.empty_cache()
                    torch.cuda.ipc_collect()