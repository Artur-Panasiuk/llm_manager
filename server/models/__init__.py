import os, importlib

for filename in os.listdir(os.path.dirname(__file__)):
    if filename.endswith(".py") and filename not in ("__init__.py", "model_base.py", "example_model.py"):
        module_name = f"{__name__}.{filename[:-3]}"
        importlib.import_module(module_name)
