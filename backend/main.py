from flask import Flask, request, jsonify
from flask_cors import CORS
from MachineLearning.classifymusic import get_genre_from_audio
import os

app = Flask(__name__)
CORS(app, supports_credentials=True)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["DEBUG"] = True

@app.route('/')
def home():
    return 'Test'

@app.route('/api/sendmp3', methods=['POST'])
def classify_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        from werkzeug.utils import secure_filename
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            genre = get_genre_from_audio(filepath)
            return jsonify({'genre': genre}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500

@app.route('/api/sendblob', methods=['POST'])
def classify_blob():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']

    if file:
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        from werkzeug.utils import secure_filename
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            genre = get_genre_from_audio(filepath)
            return jsonify({'genre': genre}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500
    