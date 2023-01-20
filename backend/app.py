import os
import tempfile
import flask
from flask import request
from flask_cors import CORS
import whisper
import datetime

app = flask.Flask(__name__)
CORS(app)
@app.route('/transcribe', methods=['POST'])
def transcribe():
    if request.method == 'POST':
        language = request.form['language']
        model = request.form['model_size']

        audio_model = whisper.load_model(model)

        temp_dir = tempfile.mkdtemp()
        save_path = os.path.join(temp_dir, 'temp.wav')

        wav_file = request.files['audio_data']
        wav_file.save(save_path)

        result = audio_model.transcribe(save_path, language='dutch')
        #save result to computer with timestamp
        save_path = os.path.join(temp_dir, 'result.txt')
        with open(save_path, 'w') as f:
            f.write(datetime.datetime.now().isoformat()+ ": " + result['text'])
        
        print(result['text'])
        return result['text']
    else:
        return "This endpoint only processes POST wav blob"


@app.route('/test', methods=['GET'])
def test():
    return "Yolo"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port)
