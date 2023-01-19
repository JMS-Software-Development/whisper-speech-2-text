import argparse
import io
import wave
import pyaudio
import os
import audioop
import tempfile
import numpy
from queue import Queue
from pydub import AudioSegment
from time import sleep
from datetime import datetime, timedelta
import speech_recognition as sr
from time import perf_counter

def main():


    def BytesToWave(bytes):
        # Write out raw frames as a wave file.
        wav_file = io.BytesIO()
        wav_writer:wave.Wave_write = wave.open(wav_file, "wb")
        wav_writer.setframerate(sample_rate)
        wav_writer.setsampwidth(pa.get_sample_size(pyaudio.paInt16))
        wav_writer.setnchannels(1)
        wav_writer.writeframes(bytes)
        wav_writer.close()

        # Read the audio data, now with wave headers.
        wav_file.seek(0)
        wav_reader:wave.Wave_read = wave.open(wav_file)
        samples = wav_reader.getnframes()
        audio = wav_reader.readframes(samples)
        wav_reader.close()

        # Convert the wave data straight to a numpy array for the model.
        # https://stackoverflow.com/a/62298670
        audio_as_np_int16 = numpy.frombuffer(audio, dtype=numpy.int16)
        audio_as_np_float32 = audio_as_np_int16.astype(numpy.float32)
        audio_normalised = audio_as_np_float32 / max_int16

        print('Audio normalized', audio_normalised)
        # Send audio normalized to whisper!!!!

    
    max_record_time = 30
    max_record_time_delta = timedelta(seconds=max_record_time)
    data_queue = Queue()
    silence_time = 1
    sample_rate = 16000
    chunk_size = 1024
    phrase1 = bytes()
    phrase2 = bytes()
    phrase1_complete = False
    phrase2_complete = False
    samples_with_silence1 = 0
    samples_with_silence2 = 0
    max_int16 = 2**15
    phrase1_record_end = datetime.utcnow() + max_record_time_delta
    phrase2_record_end = datetime.utcnow() + max_record_time_delta
    pa = pyaudio.PyAudio()

    
    stream1 = pa.open(format = pyaudio.paInt16,
                            channels = 1,
                            rate = sample_rate,
                            frames_per_buffer = chunk_size,
                            input = True,
                            input_device_index = 1)        

    stream2 = pa.open(format = pyaudio.paInt16,
                            channels = 1,
                            rate = sample_rate,
                            frames_per_buffer = chunk_size,
                            input = True,
                            input_device_index = 2)    
    while True:
        
        data1 = stream1.read(chunk_size)
        energy1 = audioop.rms(data1, pa.get_sample_size(pyaudio.paInt16))

        if energy1 > 300:
            print('Mic1 is recording')
            phrase1 += data1
            phrase1_complete = False
            samples_with_silence1 = 0
        elif energy1 < 300:
            samples_with_silence1 +=1
        
        data2 = stream2.read(1024)
        energy2 = audioop.rms(data2, pa.get_sample_size(pyaudio.paInt16))
        if energy2 > 300:
            print('Mic2 is recording')
            phrase2 += data2
            phrase1_complete = False
            samples_with_silence2 = 0
        elif energy1 < 300:
            samples_with_silence2 +=1

        #Max record time reached stopping sentance
        now = datetime.utcnow()
        if now > phrase1_record_end:
            BytesToWave(phrase1)
            phrase1_complete = True
            phrase1 = bytes()
            print('sentence 1 stopped')
            phrase1_record_end = now + max_record_time_delta
        
        if datetime.utcnow() > phrase2_record_end:
            BytesToWave(phrase2)
            phrase2_complete = True
            phrase2 = bytes()
            print('sentence 1 stopped')
            phrase2_record_end = now + max_record_time_delta
        
        
        # If we have encounter enough silence, restart the buffer and add a new line.
        if samples_with_silence1 > sample_rate / chunk_size * silence_time and not phrase1_complete:
            BytesToWave(phrase1)
            phrase1_complete = True
            phrase1 = bytes()
            print('sentence 1 ended')
            phrase1_record_end = now + max_record_time_delta


        if samples_with_silence2 > sample_rate / chunk_size * silence_time and not phrase2_complete:
            BytesToWave(phrase2)
            phrase2_complete = True
            phrase2 = bytes()
            print('sentence 2 ended')
            phrase2_record_end = now + max_record_time_delta

        
        sleep(0.25)


if __name__ == "__main__":
    main()

    # # Use AudioData to convert the raw data to wav data.
    # audio_data = sr.AudioData(last_sample, source.SAMPLE_RATE, source.SAMPLE_WIDTH)
    # wav_data = io.BytesIO(audio_data.get_wav_data())


    # # Write wav data to the temporary file as bytes.
    # with open(temp_file, 'w+b') as f:
    #     f.write(wav_data.read())











    # with mic1 as source:
    #     print("Mic1 talking")
    #     while True:
    #         # record audio stream into wav
    #         audio = r.listen(source)
    #         start = perf_counter()
    #         data = io.BytesIO(audio.get_wav_data())
    #         audio_clip = AudioSegment.from_file(data)
    #         audio_clip.export(save_path, format="wav")
    #         # use dutch model
    #         result = audio_model.transcribe(save_path, language="dutch")

    #         if not args.verbose:
    #             predicted_text = result["text"]
    #             print("Text: " + predicted_text)
    #         else:
    #             predicted_text = result["text"]
    #             end = perf_counter()
    #             duration = end-start
    #             for k,v in result.items():
    #                 print(k,v)
    #             print("Processing delay: ", duration)