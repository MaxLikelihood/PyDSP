from config import audio as config_audio
import numpy
from scipy import signal
from scipy.fftpack import rfft

class audio(object):

    @staticmethod
    def __decode_data(data):
        # Decode & store decoded audio data as new key:value pair in dictionary
        # Parameters: data: [{'frame_data': string,
        #                     'frame_count': int,
        #                     'frame_time': float,
        #                     'frame_position': int}, ...]

        # decode according to specified type in config
        for i in range(len(data)):
            data[i]['frame_decoded'] = numpy.fromstring(data[i]['frame_data'],
                                                        dtype = config_audio.decoding_format,
                                                        count = data[i]['frame_count'])

    @staticmethod
    def __window_data(data):
        # Apply window function to the decoded data & store as new key:value pair in dictionary
        # Parameters: data: [{'frame_data': string,
        #                     'frame_count': int,
        #                     'frame_time': float,
        #                     'frame_position': int,
        #                     'frame_decoded': type}, ...]

        # cache window function
        if 'hann' == config_audio.frame_window:
            window = signal.hann(config_audio.frames_per_buffer)
        elif 'hamming' == config_audio.frame_window:
            window = signal.hamming(config_audio.frames_per_buffer)
        elif 'blackman' == config_audio.frame_window:
            window = signal.blackman(config_audio.frames_per_buffer)
        elif 'bartlett' == config_audio.frame_window:
            window = signal.bartlett(config_audio.frames_per_buffer)
        elif 'barthann' == config_audio.frame_window:
            window = signal.barthann(config_audio.frames_per_buffer)
        else:
            # window function unavailable
            return

        # apply specified window function in config
        for i in range(len(data)):
            data[i]['frame_windowed'] = data[i]['frame_decoded'][:] * window


    @staticmethod
    def analyze(data):
        # Decode & window raw audio data
        audio.__decode_data(data)
        audio.__window_data(data)

    @staticmethod
    def __rfft_data(data):
        # Apply discrete fourier transform on windowed audio data & store as new key:value pair in dictionary
        # Parameters: data: [{'frame_data': string,
        #                     'frame_count': int,
        #                     'frame_time': float,
        #                     'frame_position': int,
        #                     'frame_decoded': type
        #                     'frame_windowed': type}, ...]

        for i in range(len(data)):
            data[i]['frame_rfft'] = rfft(data[i]['frame_windowed'])


