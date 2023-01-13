import os
import tempfile
import flask
from flask import request
from flask_cors import CORS
import whisper

app = flask.Flask(__name__)
CORS(app)


@app.route('/transcribe', methods=['POST'])
def transcribe():
    if request.method == 'POST':
        language = request.form['language']
        model = request.form['model_size']

        # there are no english models for large
        # if model != 'large' and language == 'english':
        #     model = model + '.en'
        # we are using the dutch model so we don't need to add .en

        audio_model = whisper.load_model(model)

        temp_dir = tempfile.mkdtemp()
        save_path = os.path.join(temp_dir, 'temp.wav')

        wav_file = request.files['audio_data']
        wav_file.save(save_path)

        result = audio_model.transcribe(save_path, language='dutch')
        return result['text']
    else:
        return "This endpoint only processes POST wav blob"
