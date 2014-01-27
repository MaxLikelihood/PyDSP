import pyaudio

class audio(object):

    host_api = 'ALSA'
    host_api_device = 'default'
    sampling_rate = 44100
    input_channels = 1
    sampling_format = pyaudio.paFloat32
    frames_per_buffer = 1024