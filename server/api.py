from flask import Flask, request, jsonify
from queue_manager import waiting_queue, done_queue
from models.model_base import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/models', methods=['GET'])
def get_models():
    return jsonify(BaseModel.available_models())

@app.route('/request', methods=['POST'])
def handle_request():
    data = request.get_json()
    required = {'task_id', 'model_name', 'prompt', 'tokens'}

    if not required.issubset(data):
        return jsonify(error='Missing fields'), 400

    waiting_queue.put({
        'task_id': data['task_id'],
        'model_name': data['model_name'],
        'prompt': data['prompt'],
        'tokens': data['tokens']
    })

    return jsonify(status='queued', task_id=data['task_id']), 202

@app.route('/get/<task_id>', methods=['GET'])
def get_result(task_id):
    if task_id in done_queue:
        return jsonify({
            'status': 'done',
            'task_id': task_id,
            'result': done_queue[task_id]
        }), 200
    else:
        return jsonify({
            'status': 'pending',
            'task_id': task_id,
            'message': 'Still processing or not found'
        }), 202

def start_server():
    app.run(host=os.getenv("NETWORK_IP"), port=os.getenv("NETWORK_PORT"), debug=False)