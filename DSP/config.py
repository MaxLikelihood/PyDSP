import pyaudio

class audio(object):

    host_api = 'ALSA'
    host_api_device = 'Scarlett 2i2 USB: USB Audio (hw:1,0)'
    sampling_rate = 44100
    input_channels = 1
    sampling_format = pyaudio.paFloat32
    frames_per_buffer = 1024