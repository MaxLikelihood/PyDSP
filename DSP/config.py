import pyaudio

class config(object):

    global host_api
    global host_api_device
    global sampling_rate
    global input_channels
    global sampling_format

    def __init__(self):
        self.host_api = 'ALSA'
        self.host_api_device = 'redbox'
        self.sampling_rate = 44100
        self.input_channels = 1
        self.sampling_format = pyaudio.paFloat32