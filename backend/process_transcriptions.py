import os
from queue import Queue
from threading import Thread
import time 
from data import *


dataQueue = Queue()

def t_thread():
    print("Starting transcriptions processing thread")
    while True:
        time.sleep(1)
        onlyfiles = list_files(TRANSSCRIPTIONS_FOLDER)
        if len(onlyfiles) > 0:
            prompt = ''
            with open(TRANSSCRIPTIONS_FOLDER + "/" + onlyfiles[0], 'r') as f:
                prompt = f.read()
                print(f"Considering promt: {prompt}")
                accepted = len(prompt) > 3
                if accepted:
                    print("Accepted")
                else:
                    print("Rejected")

            with open(ACCEPTED_TRANSACRIPTIONS_FOLDER + "/" + onlyfiles[0], 'w') as f:
                f.write(prompt)
            
            os.remove(TRANSSCRIPTIONS_FOLDER + "/" + onlyfiles[0]) 


if __name__ == "__main__":
    transcriber = Thread(target=t_thread)
    transcriber.start()





    



