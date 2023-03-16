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
from os import listdir
from os.path import isfile, join

dataQueue = Queue()

def transcribe_thread():
    print("Starting transcribing thread")
    while True:
        time.sleep(1)
        onlyfiles = list_files(ACCEPTED_TRANSACRIPTIONS_FOLDER)
        if len(onlyfiles) > 0:
            prompt = ''
            with open(ACCEPTED_TRANSACRIPTIONS_FOLDER + "/" + onlyfiles[0], 'r') as f:
                prompt = f.read()
                print(f"Generating image for promt: {prompt}")
                image = generateImage(prompt)
                image.save(IMAGES_FOLDER + "/" + onlyfiles[0] + ".png")

            with open(DONE_TRANSCRIPTIONS_FOLDER + "/" + onlyfiles[0], 'w') as f:
                f.write(prompt)
            
            os.remove(ACCEPTED_TRANSACRIPTIONS_FOLDER + "/" + onlyfiles[0])


if __name__ == "__main__":
    transcriber = Thread(target=transcribe_thread)
    transcriber.start()

