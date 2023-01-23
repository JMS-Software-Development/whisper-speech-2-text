# -*- coding: utf-8 -*-
"""
Created on Fri Jan 20 17:01:52 2023

@author: olivi
"""
import argparse
import io
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import tempfile
import datetime
import os
import requests
from time import perf_counter

for index, mic in enumerate(sr.Microphone.list_microphone_names()):
    print("Microphone " +str(index) +": "+str(mic))

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("--mic_index", help="index corresponding to microphone input for audio recording", type=int )
parser.add_argument("--energy", default=500,
                    help="Energy level for mic to detect", type=int)
parser.add_argument("--dynamic_energy", default=False,
                    help="Flag to enable dynamic energy", type=bool)
parser.add_argument("--pause", default=0.8,
                    help="Minimum length of silence (sec) that will register as the end of a phrase", type=float)
# parser.add_argument("--verbose", default=False,
#                     help="Whether to print verbose output", type=bool)
args = parser.parse_args()


#create folder tmp with mic index
folder_name = "mic" + str(args.mic_index)
os.makedirs(folder_name, exist_ok=True)
save_path = folder_name

def transcribe():

    # for testing
    # audio_model = whisper.load_model('tiny')

    # load the speech recognizer with CLI settings
    r = sr.Recognizer()
    r.energy_threshold = args.energy
    r.pause_threshold = args.pause
    r.dynamic_energy_threshold = args.dynamic_energy
    with sr.Microphone(sample_rate=16000, device_index=args.mic_index) as source:
        print("Let's get the talking going! Listening to mic: ", args.mic_index)
        start_time = datetime.datetime.now()
        while True:
            # record audio stream into wav
            audio = r.listen(source, phrase_time_limit=10)
            #print time delta
            print("Time delta: ", datetime.datetime.now()-start_time)
            start = perf_counter()
            data = io.BytesIO(audio.get_wav_data())
            audio_clip = AudioSegment.from_file(data)
            save_path = os.path.join(folder_name, "recording"+datetime.datetime.now().isoformat()+".wav")
            audio_clip.export(save_path, format="wav")
            

            # #TODO create request to backend
            # files = {'upload_file': open("recordings_" + str(args.mic_index) + "/temp.wav",'rb')}
            # url = ""
            # requests.post(url, files=files)
            
            # for testing
            # result = audio_model.transcribe(save_path, language="dutch")

            # if not args.verbose:
            #     predicted_text = result["text"]
            #     print("Text: " + predicted_text)
            # else:
            #     predicted_text = result["text"]
            #     end = perf_counter()
            #     duration = end-start
            #     for k,v in result.items():
            #         print(k,v)
            #     print("Processing delay: ", duration)

if __name__ == "__main__":
    transcribe()
    print("\n--> How cool was that?!")