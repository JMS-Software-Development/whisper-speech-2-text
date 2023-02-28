from os import listdir
from os.path import isfile, join

TRANSSCRIPTIONS_FOLDER="./transcriptions"
ACCEPTED_TRANSACRIPTIONS_FOLDER = './accepted_transcriptions'
DONE_TRANSCRIPTIONS_FOLDER = './completed_transcriptions'

RECORDING_FOLDER = './recordings'
IMAGES_FOLDER = "./generated_images"

def list_files(folder):
    return [f for f in listdir(folder) if isfile(join(folder, f)) and f != ".gitkeep"]