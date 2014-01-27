from multiprocessing import Process, Pool, Queue, Pipe, Lock
import pyaudio
import numpy
import scipy
import time
import sys

sampling_rate = 44100
input_channel = 2
frames_per_buffer = 1024

# define callback function
def callback(in_data, frame_count, time_info, status_flags):
    
    return (None, pyaudio.paContinue)

# instantiate PyAudio
p = pyaudio.PyAudio()

default_input_device_info = p.get_default_input_device_info()

stream = p.open(rate = sampling_rate,
                channels = input_channel,
                format = pyaudio.paFloat32,
                input = True,
                output = False,
                input_device_index = default_input_device_info['index'],
                output_device_index = None,
                frames_per_buffer = frames_per_buffer,
                start = False,
                stream_callback = callback)

print "\nStarting Stream"
stream.start_stream()

# stream active
time.sleep(1)

print "\nClosing Stream"
stream.close()

# terminate PyAudio
p.terminate()