import pyaudio
import sys
import numpy as np
import aubio

import asyncio
from light import light_random, lights_random, lights_off, lights_normal

# initialise pyaudio
p = pyaudio.PyAudio()

# open stream
#buffer_size = 1024
buffer_size = 1024 // 2
pyaudio_format = pyaudio.paFloat32
n_channels = 1
samplerate = 44100
stream = p.open(format=pyaudio_format,
                channels=n_channels,
                rate=samplerate,
                input=True,
                frames_per_buffer=buffer_size)

# run forever
outputsink = None
record_duration = None

# setup pitch
tolerance = 0.8
#win_s = 4096 # fft size
win_s = 1024 # fft size
hop_s = buffer_size # hop size
pitch_o = aubio.pitch("default", win_s, hop_s, samplerate)
a_tempo = aubio.tempo("default", win_s, hop_s, samplerate)
pitch_o.set_unit("midi")
pitch_o.set_tolerance(tolerance)

sinceBeat = 0
pitch = 0
volume = 0

counter = 0

print("*** starting recording")
asyncio.run(lights_random())
freq = 1
while True:
    try:
        audiobuffer = stream.read(buffer_size, exception_on_overflow=False)
        signal = np.fromstring(audiobuffer, dtype=np.float32)

        #pitch += pitch_o(signal)[0]
        #confidence = pitch_o.get_confidence()
        #volume += aubio.level_lin(signal)

        #sinceBeat += 1

        is_beat = a_tempo(signal)
        if is_beat:
            counter += 1
            #print(f'Beat {counter}!')
            if counter == freq:
                asyncio.run(light_random(0))

                # Empirically determined to be roughly normalized around 0-1
                # Pitch optimally evenly distributed, volume optimally near 1
                # print (f'Pitch: {0.015*pitch/sinceBeat}')
                # print (f'Volume: {10*volume/sinceBeat}')
                # pitch = 0
                # volume = 0
                # sinceBeat = 0
                # counter = 0
            elif counter == 2*freq:
                asyncio.run(light_random(1))
            elif counter == 3*freq:
                asyncio.run(light_random(2))
                counter = 0

        #print("{} / {}".format(pitch,confidence))

    except KeyboardInterrupt:
        print("*** Ctrl+C pressed, exiting")
        break

print("*** done recording")
asyncio.run(lights_normal())
stream.stop_stream()
stream.close()
p.terminate()
