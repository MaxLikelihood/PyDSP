import pyaudio

class config(object):

    global host_API
    global sampling_Rate
    global input_Channels
    global sampling_Format
    
    def __init__(self):
        self.host_API = 'ALSA'
        self.sampling_Rate = 44100
        self.input_Channels = 1
        self.sampling_Format = pyaudio.paFloat32