from flask import Flask, request, jsonify
from MachineLearning.classifymusic import get_genre_from_audio
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["DEBUG"] = True

@app.route('/')
def home():
    return 'Test'

@app.route('/api/sendmp3', methods =['POST'])
def calssify_audio():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    user = request.form.get('user')
    
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        
        try:
            genre = get_genre_from_audio(filepath, user)
            return jsonify({'genre': genre}), 200
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run()
