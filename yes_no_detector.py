#!/usr/bin/env python3
from scipy.io import wavfile as wav
import pyaudio
import wave
import numpy as np
import matplotlib.pyplot as plt

while True:
    FORMAT = pyaudio.paInt16  # format of sampling 16 bit int
    CHANNELS = 1  # number of channels it means number of sample in every sampling
    RATE = 44100  # number of sample in 1 second sampling
    CHUNK = 1024  # length of every chunk
    RECORD_SECONDS = 1  # time of recording in seconds
    WAVE_OUTPUT_FILENAME = "file.wav"  # file name

    audio = pyaudio.PyAudio()

    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    # print("recording...")
    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    # print("finished recording")

    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # storing voice
    waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    # reading voice
    rate, data = wav.read('file.wav')
    # data is voice signal. its type is list(or numpy array)

    # -----------------------------------------------------------------------------------

    MinF = 800
    MaxF = 3000
    BanF = 1520
    SenF = 1700000000000
    Err = 10
    Yes = 0
    No = 0

    Total = np.power(abs(np.fft.fft(data)), 2)

    for i in range(MinF, MaxF):
        if Total[i] > SenF:
            if i > BanF:
                Yes = Yes + 1
            if i < BanF:
                No = No + 1

    if No > Yes + Err:
        print("No")
    if Yes > No + Err:
        print("Yes")
