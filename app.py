from flask import Flask, request, jsonify, send_from_directory
import requests
import base64
import os

app = Flask(__name__, static_folder='static')

REMOVE_BG_API_KEY = "UnCRQ1Sxa5UhadPa7MFKZBDQ"

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    data = request.get_json()
    image_data = data.get('image')

    if not image_data:
        return jsonify({'error': 'No image provided'}), 400

    # Extract base64 data
    if ',' in image_data:
        image_base64 = image_data.split(',')[1]
    else:
        image_base64 = image_data

    try:
        image_bytes = base64.b64decode(image_base64)
    except Exception as e:
        return jsonify({'error': 'Invalid image format'}), 400

    response = requests.post(
        'https://api.remove.bg/v1.0/removebg',
        headers={'X-Api-Key': REMOVE_BG_API_KEY},
        files={'image_file': ('image.jpg', image_bytes)},
        data={'size': 'auto'}
    )

    if response.status_code == requests.codes.ok:
        result_b64 = "data:image/png;base64," + base64.b64encode(response.content).decode()
        return jsonify({'result': result_b64})
    else:
        return jsonify({'error': 'Remove.bg API error', 'message': response.text}), 500
