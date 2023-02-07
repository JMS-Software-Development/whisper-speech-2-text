 
import torch
from torch import autocast
from diffusers import StableDiffusionPipeline
from queue import Queue
import time

class DataStore():
    language = "dutch"
    model = "small"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("Using device: ", device)
    pipe = StableDiffusionPipeline.from_pretrained(
        'hakurei/waifu-diffusion',
        torch_dtype=torch.float32
    )

t = time.time()
data = DataStore()
print(f"Loading model took {time.time() - t} seconds")

dataQueue = Queue()

prompt = "1girl, aqua eyes, baseball cap, blonde hair, closed mouth, earrings, green background, hat, hoop earrings, jewelry, looking at viewer, shirt, short hair, simple background, solo, upper body, yellow shirt"
# with autocast("gpu"):
image = data.pipe(prompt, guidance_scale=6)[0][0]

print(image)
    
image.save("test.png")