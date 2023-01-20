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
import os
import requests
from time import perf_counter

print("All connected microphones: ", sr.Microphone.list_microphone_names())
print("All connected microphones: ", str(sr.Microphone.list_working_microphones()))

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("--mic_index", default=1, help="index corresponding to microphone input for audio recording", type=int )
parser.add_argument("--energy", default=500,
                    help="Energy level for mic to detect", type=int)
parser.add_argument("--dynamic_energy", default=False,
                    help="Flag to enable dynamic energy", type=bool)
parser.add_argument("--pause", default=0.8,
                    help="Minimum length of silence (sec) that will register as the end of a phrase", type=float)
args = parser.parse_args()


temp_dir = "recordings_" + str(args.mic_index)
save_path = os.path.join(temp_dir, "temp.wav")

def check_stop_word(predicted_text: str) -> bool:
    import re
    pattern = re.compile('[\W_]+', re.UNICODE) 
    return pattern.sub('', predicted_text).lower() == args.stop_word

def transcribe():
    # load the speech recognizer with CLI settings
    r = sr.Recognizer()
    r.energy_threshold = args.energy
    r.pause_threshold = args.pause
    r.dynamic_energy_threshold = args.dynamic_energy
    # TODO:check how it knows when sentence is done
    # TODO:whene max time is reached, stop sentence
    # TODO: How does with work?
    with sr.Microphone(sample_rate=16000, device_index=args.mic_index) as source:
        print("Let's get the talking going! Listening to mic: ", args.mic_index)
        while True:
            # record audio stream into wav
            audio = r.listen(source)
            start = perf_counter()
            data = io.BytesIO(audio.get_wav_data())
            audio_clip = AudioSegment.from_file(data)
            audio_clip.export(save_path, format="wav")
            

            #TODO create request to backend
            files = {'upload_file': open("recordings_" + str(args.mic_index) + "/temp.wav",'rb')}
            url = ""
            requests.post(url, files=files)

            
            
            


if __name__ == "__main__":
    transcribe()
    print("\n--> How cool was that?!")