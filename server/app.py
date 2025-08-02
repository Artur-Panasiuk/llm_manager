from flask import Flask, request, jsonify
from model_handler import load_models_config

app = Flask(__name__)

queue = []

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
    if not all(k in data for k in ('id', 'model', 'prompt')):
        return jsonify({'error': 'Missing fields'}), 400

    queue.append({
        'model': data['model'],
        'prompt': data['prompt']
    })

    print(queue)

    # results[data['id']] = process_prompt(data['model'], data['prompt'])

    return jsonify({'status': 'queued', 'id': data['id']}), 202

if __name__ == '__main__':
    app.run(debug=False)
