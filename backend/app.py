import os
import tempfile
import flask
from flask import request
from flask_cors import CORS
import whisper

app = flask.Flask(__name__)
CORS(app)


class DataStore():
    language = "dutch"
    model = "medium"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    audio_model = whisper.load_model(model, langauge=language)

data = DataStore()

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if request.method == 'POST':
        #language = request.form['language']
        #model = request.form['model_size']

        audio_model = data.audio_model

        temp_dir = tempfile.mkdtemp()
        save_path = os.path.join(temp_dir, 'temp.wav')

        wav_file = request.files['audio_data']
        wav_file.save(save_path)

        result = audio_model.transcribe(save_pat)
        return result['text']
    else:
        return "This endpoint only processes POST wav blob"


@app.route('/test', methods=['GET'])
def test():
    return "Yolo"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port)
