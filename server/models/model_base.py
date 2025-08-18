class BaseModel:
    registry = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseModel.registry[cls.__name__.lower()] = cls

    @classmethod
    def create(cls, name, *args, **kwargs):
        if name.lower() not in cls.registry:
            raise ValueError(f"Nieznany model: {name}")
        return cls.registry[name.lower()](*args, **kwargs)
    
    @classmethod
    def available_models(cls):
        return list(cls.registry.keys())