from flask import Flask, request, jsonify
from model_handler import load_models_config, get_model_by_id

queue = []

app = Flask(__name__)

model_data = load_models_config()

@app.route('/queue', methods=['GET'])
def get_queue():
    return jsonify(queue)

@app.route('/models', methods=['GET'])
def get_models():
    return jsonify([(model['id'], model['name']) for model in model_data])

@app.route('/request', methods=['POST'])
def handle_request():
    data = request.get_json()
    required = {'task_id', 'model_id', 'prompt'}

    if not required.issubset(data):
        return jsonify(error='Missing fields'), 400

    queue.append({k: data[k] for k in ('task_id', 'model_id', 'prompt')})

    return jsonify(status='queued', id=data['task_id']), 202


if __name__ == '__main__':
    app.run(debug=False)