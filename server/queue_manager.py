from queue import Queue
from models.model_base import BaseModel
import models

done_queue = {}
waiting_queue = Queue()

def queue_handler():
    while True:
        task = waiting_queue.get()
        model = BaseModel.create(task["model_name"])
        model.load()
        done_queue[task["task_id"]] = model.prompt(task["prompt"], int(task["tokens"]))