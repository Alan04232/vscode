import sounddevice as sd
import numpy as np

def callback(indata, frames, time, status):
    print("Audio chunk received")

sd.InputStream(channels=1, callback=callback, device="WO Mic virtual device").start()
