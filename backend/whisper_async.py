import argparse
import io
from pydub import AudioSegment
import speech_recognition as sr
import whisper
import tempfile
import os

temp_dir = tempfile.mkdtemp()
save_path = os.path.join(temp_dir, "temp.wav")


def check_stop_word(predicted_text: str, stop_word: str) -> bool:
    import re
    pattern = re.compile('[\W_]+', re.UNICODE)
    return pattern.sub('', predicted_text).lower() == stop_word


def transcribe(model, language, mic_energy, pause_duration, mic_dynamic_energy, stop_word):
    # there are no english models for large
    # if model != "large" and language == 'english':
    #     model = model + ".en"
    # we are using the dutch model so we don't need to add .en

    audio_model = whisper.load_model(model)

    r = sr.Recognizer() # added audio reconizer wasn't in the original async code --Milan
    r.energy_threshold = mic_energy
    r.pause_threshold = pause_duration
    r.dynamic_energy_threshold = mic_dynamic_energy
    
    with sr.Microphone(sample_rate=16000) as source:
        print("Let's get the talking going!")
        while True:
            # record audio stream into wav
            audio = r.listen(source)
            data = io.BytesIO(audio.get_wav_data())
            audio_clip = AudioSegment.from_file(data)
            audio_clip.export(save_path, format="wav")
            # use dutch model
            result = audio_model.transcribe(save_path, language="dutch")
  
            predicted_text = result["text"]
            print("Text: " + predicted_text)

            # if check_stop_word(predicted_text, stop_word):
            #     break
