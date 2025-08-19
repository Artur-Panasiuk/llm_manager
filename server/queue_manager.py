from queue import Queue
from models.model_base import BaseModel
import models

done_queue = {}
waiting_queue = Queue()

current_model = None
current_model_name = None

def queue_handler():
    global current_model, current_model_name

    while True:
        task = waiting_queue.get()
        required_model_name = task["model_name"]

        if current_model is None or current_model_name != required_model_name:
            if current_model is not None:
                current_model.clear_memory()
            
            current_model = BaseModel.create(required_model_name)
            current_model.load()
            current_model_name = required_model_name

        result = current_model.prompt(task["prompt"], int(task["tokens"]))
        done_queue[task["task_id"]] = result