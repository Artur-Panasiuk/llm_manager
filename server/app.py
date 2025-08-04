from flask import Flask, request, jsonify
from model_handler import load_models_config, get_model_by_id, load_model_and_tokenizer, clear_memory
from prompt_model import prompt_llama, prompt_qwen
from threading import Thread
from queue import Queue
import time

app = Flask(__name__)

task_queue = Queue()
completed_tasks = {}

model_data = load_models_config()

# TEMP
current_model = None
model = None
tokenizer = None

@app.route('/queue', methods=['GET'])
def get_queue():
    return jsonify(task_queue)

@app.route('/models', methods=['GET'])
def get_models():
    return jsonify([(model['id'], model['name']) for model in model_data])

@app.route('/request', methods=['POST'])
def handle_request():
    data = request.get_json()
    required = {'task_id', 'model_id', 'prompt'}

    if not required.issubset(data):
        return jsonify(error='Missing fields'), 400

    task_queue.put({
        'task_id': data['task_id'],
        'model_id': data['model_id'],
        'prompt': data['prompt']
    })

    return jsonify(status='queued', task_id=data['task_id']), 202

@app.route('/get/<task_id>', methods=['GET'])
def get_result(task_id):
    if task_id in completed_tasks:
        return jsonify({
            'status': 'done',
            'task_id': task_id,
            'result': completed_tasks[task_id]
        }), 200
    else:
        return jsonify({
            'status': 'pending',
            'task_id': task_id,
            'message': 'Still processing or not found'
        }), 202

def start_server():
    app.run(debug=False)

def ai_worker(queue):
    global tokenizer, model

    while True:
        task = queue.get()
        print(f"Processing task {task['task_id']}...")

        #TEMPORARY HANDLING

        current_model_data = get_model_by_id(model_data, int(task['model_id']))

        if current_model == None:
            tokenizer, model = load_model_and_tokenizer(current_model_data['path'])
        elif current_model != (task['model_id']):
            clear_memory(model, tokenizer)
            tokenizer, model = load_model_and_tokenizer(current_model_data['path'])

        res = "" 

        if current_model_data['type'] == 'qwen':
            res = prompt_qwen(tokenizer, model, task['prompt'])
        elif current_model_data['type'] == 'llama':
            res = prompt_llama(tokenizer, model, task['prompt'])

        completed_tasks[task['task_id']] = res
        print(f"Task {task['task_id']} completed.")

        queue.task_done()

if __name__ == '__main__':
    Thread(target=start_server, daemon=True).start()
    Thread(target=ai_worker, args=(task_queue,), daemon=True).start()

    while True:
        time.sleep(1)