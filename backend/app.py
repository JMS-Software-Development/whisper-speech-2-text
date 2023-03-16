import os
from queue import Queue
import tempfile
import flask
from flask import request
import datetime
import wave
from threading import Thread
from flask_cors import CORS
import whisper
import torch
import time 
from stable_diffusion.generate import generateImage
from data import *

app = flask.Flask(__name__)
CORS(app)
class DataStore():
    language = "dutch"
    # print("models available", whisper.available_models())
    model = "large" #tiny, base, small, medium, large, large-v1, large-v2
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using device: ", device)
    audio_model = whisper.load_model(model)


t = time.time()
data = DataStore()
print(f"Loading model took {time.time() - t} seconds")

dataQueue = Queue()


def transcribe_thread():
    print("Starting transcribing thread")
    start_generating = time.time()
    while True:
        if dataQueue.empty():
            # print("No audio data in queue")
            time.sleep(1)
        else:
            start_time = time.time()
            print("Starting transcribing")
            audio_model = data.audio_model
            save_path = dataQueue.get()

            result = audio_model.transcribe(save_path, language='dutch', fp16=False)

            recording_id = save_path.split("-")[1]
            print(f"Transcribing took {time.time() - start_time} seconds")
            print("Resut: " + result['text'])
            if len(result['text'].strip()) > 0:
                save_path = os.path.join(TRANSSCRIPTIONS_FOLDER, recording_id + "-" + datetime.datetime.now().isoformat()+".txt")
                with open(save_path, 'w') as f:
                    f.write(result['text'].strip())
            
            if time.time() - start_generating > 240:
                start_generating = time.time()
                generateImage(result['text'])

transcriber = Thread(target=transcribe_thread)
transcriber.start()

recording_index = 0
@app.route('/transcribe/<mic>', methods=['POST'])
def addToQueue(mic):
    global recording_index
    if request.method == 'POST':
        #language = request.form['language']
        #model = request.form['model_size']
        os.makedirs(RECORDING_FOLDER+str(mic), exist_ok=True)
        save_path = os.path.join(RECORDING_FOLDER+str(mic), f"recording-{recording_index}-"+datetime.datetime.now().isoformat()+".wav")
        recording_index += 1
        with open(save_path, 'wb') as f:
            f.write(request.data)

        dataQueue.put(save_path)

        print(f"Added to queue, now size: {dataQueue.qsize()}")
        return f"Added to queue ({dataQueue.qsize()})"
    else:
        return "This endpoint only processes POST wav blob"

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 8000))
    app.run(debug=True, host='0.0.0.0', port=port)





    



