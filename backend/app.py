import os
from queue import Queue
import tempfile
import flask
from flask import request
import datetime
from threading import Thread
from flask_cors import CORS
import whisper
import torch
import time 

app = flask.Flask(__name__)
CORS(app)
class DataStore():
    language = "dutch"
    model = "small"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using device: ", device)
    audio_model = whisper.load_model(model)


t = time.time()
data = DataStore()
print(f"Loading model took {time.time() - t} seconds")

dataQueue = Queue()

def transcribe_thread():
    print("Starting transcribing thread")
    while True:
        if dataQueue.empty():
            print("No audio data in queue")
            time.sleep(1)
        else:
            start_time = time.time()
            print("Startinhg transcribing")
            audio_model = data.audio_model
            save_path = dataQueue.get()

            result = audio_model.transcribe(save_path, language='dutch')

            print(result['text'])
            print(f"Transcribing took {time.time() - start_time} seconds")
            print(result['text'])

transcriber = Thread(target=transcribe_thread)
transcriber.start()
folder_name = "recordings"
os.makedirs(folder_name, exist_ok=True)

@app.route('/transcribe', methods=['POST'])
def addToQueue():
    if request.method == 'POST':
        #language = request.form['language']
        #model = request.form['model_size']
        save_path = os.path.join(folder_name, "recording"+datetime.datetime.now().isoformat()+".wav")
        wav_file = request.files['audio_data']
        wav_file.save(save_path)
        dataQueue.put(save_path)

        print("Added to queue")
        print(dataQueue.qsize())
        return "Added to queue"
    else:
        return "This endpoint only processes POST wav blob"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port)





    



