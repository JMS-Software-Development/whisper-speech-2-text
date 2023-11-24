import argparse
import io
from pydub import AudioSegment
import speech_recognition as sr
import tempfile
import os
from time import perf_counter
import requests
from dotenv import load_dotenv
load_dotenv()

#key for sebastiaan@anansiwebdevelopment.nl

api_key = os.getenv('OPENAI_KEY')
from openai import OpenAI
save_to_relative_path = "generated_images/"


parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--model", default="base", help="Model to use",
                    choices=["tiny", "base", "small", "medium", "large"])
parser.add_argument("--english", default=True,
                    help="Whether to use English model", type=bool)
parser.add_argument("--stop_word", default="stop",
                    help="Stop word to abort transcription", type=str)
parser.add_argument("--verbose", default=False,
                    help="Whether to print verbose output", type=bool)
parser.add_argument("--energy", default=500,
                    help="Energy level for mic to detect", type=int)
parser.add_argument("--dynamic_energy", default=False,
                    help="Flag to enable dynamic energy", type=bool)
parser.add_argument("--pause", default=0.8,
                    help="Minimum length of silence (sec) that will register as the end of a phrase", type=float)
args = parser.parse_args()


temp_dir = tempfile.mkdtemp()
save_path = os.path.join(temp_dir, "temp.wav")

print("SAVE PATH: " + save_path)

def check_stop_word(predicted_text: str) -> bool:
    import re
    pattern = re.compile('[\W_]+', re.UNICODE)
    return pattern.sub('', predicted_text).lower() == args.stop_word

def transcribe():
    model = args.model
    # there are no english models for large
    # if args.model != "large" and args.english:
        # model = model + ".en"
    # audio_model = whisper.load_model(model)

    # load the speech recognizer with CLI settings
    r = sr.Recognizer()
    #r.energy_threshold = args.energy
    #r.pause_threshold = args.pause
    #r.dynamic_energy_threshold = args.dynamic_energy

    with sr.Microphone() as source:
        print("Let's get the talking going!")
        while True:
            # record audio stream into wav
            audio = r.listen(source)
            start = perf_counter()
            data = io.BytesIO(audio.get_wav_data())
            audio_clip = AudioSegment.from_file(data)
            audio_clip.export(save_path, format="wav")

            #transcribe using whisper api
            audio_file= open(save_path, "rb")
            transcript = client.audio.transcriptions.create(model="whisper-1", file=audio_file, response_format="text")
            print(transcript)
            result = transcript

            if not args.verbose:
                predicted_text = result
                print("Text: " + predicted_text)
            else:
                predicted_text = result
                end = perf_counter()
                duration = end-start
                for k,v in result.items():
                    print(k,v)
                print("Processing delay: ", duration)
            if "Thank you for watching" in predicted_text:
                continue #skip this transcription, which often arises when no text is predicted
            if len(predicted_text) > 1:
                #transcription2imageprompt
                image_prompt = get_prompt(predicted_text)

                #imageprompt2image
                # Make API call to get image
                response = client.images.generate(
                  prompt= image_prompt,
                  n=1,
                  size= "512x512"
                )
                img_data = requests.get(response.data[0].url).content
                print(response.data[0].url)
                img_name = image_prompt.replace(' ', '_').replace('.','').replace(',','') + ".png"
                with open(save_to_relative_path + img_name, 'wb') as handler:
                    handler.write(img_data)
                print("image downloaded")

            if check_stop_word(predicted_text):
                break

def get_prompt(transcription, add_imagery=False):
    prompt = "DEFAULT PROMPT " + transcription
    prompt_extension_extra_imagery = ""
    if add_imagery:
        prompt_extension_extra_imagery = " and using imagery sourced from"

    response = client.chat.completions.create(model='gpt-3.5-turbo', messages=[{"role": "user", "content": "Could the following message easily and unambiguously be translated to a painting by a human? Message = " + transcription + ". Please answer only with yes or no."}])
    print(response.choices[0].message.content)
    if response.choices[0].message.content == "Yes.":
        response = client.chat.completions.create(model='gpt-3.5-turbo', messages=[{"role": "user", "content": "the following message will be used as an image caption, it should be descriptive, very short and concise and only contain information present in the message. Please return a more adequate version of this caption. Return only a single improved caption, nothing else. Message = " + transcription + "."}])
        prompt= response.choices[0].message.content
    elif response.choices[0].message.content == "No.":
        #response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=[{"role": "user", "content": "Using nouns and adjectives sourced from the message: Answer with only a very short and concise description of a (not necessarily realistic) setting closely related to" + prompt_extension_extra_imagery + " this Message = " + self.transcription + "."}])
        response = client.chat.completions.create(model='gpt-3.5-turbo', messages=[{"role": "user", "content": "Your task is to provide a short and concise description of a setting that is directly inspired by a given message. Specifically, for the message '" + transcription + "', please provide a setting that you think closely relates to this message without adding any new information. The setting does not have to be realistic, and should be based solely on the message and should not include any additional details that are not already implied by the message. Your response should be brief and to the point."}])
        prompt= response.choices[0].message.content
        if len(prompt) > 200:
            print("long answer: " + prompt)
            response = client.chat.completions.create(model='gpt-3.5-turbo', messages=[{"role": "user", "content": "Using nouns and adjectives sourced from the message, return a very short and consise summary of this message: " + transcription + "."}])
            prompt= response.choices[0].message.content
    prompt = prompt.replace('"', '')
    print("Resulting prompt: " + prompt)
    return prompt

if __name__ == "__main__":
    transcribe()
    print("\n--> How cool was that?!")
