import pyaudio

class audio(object):

    host_api = 'ALSA'
    # host_api_device = 'Scarlett 2i2 USB: USB Audio (hw:1,0)'
    host_api_device = 'default'
    sampling_rate = 44100
    input_channels = 1
    sampling_format = pyaudio.paFloat32
    decoding_format = 'Float32'
    frame_window = 'hann'
    frames_per_buffer = 1024