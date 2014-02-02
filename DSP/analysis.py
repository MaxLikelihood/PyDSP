from config import audio as config_audio
from config import analysis as config_analysis
import numpy
import scipy
from scipy import signal
from scipy.fftpack import rfft

class audio(object):

    # mapping of rfft bin indexes to corresponding frequencies
    __rfft_freq_index = []
    # mapping of frequencies to corresponding rfft bin indexes
    __rfft_bin_index = []

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
                                                        dtype = config_analysis.decoding_format,
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
        if 'hann' == config_analysis.frame_window:
            window = signal.hann(config_audio.frames_per_buffer)
        elif 'hamming' == config_analysis.frame_window:
            window = signal.hamming(config_audio.frames_per_buffer)
        elif 'blackman' == config_analysis.frame_window:
            window = signal.blackman(config_audio.frames_per_buffer)
        elif 'bartlett' == config_analysis.frame_window:
            window = signal.bartlett(config_audio.frames_per_buffer)
        elif 'barthann' == config_analysis.frame_window:
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
        # Perform rfft on windowed data
        audio.__rfft_data(data)
        # Compute magnitude from rfft coefficients
        audio.__magn_data(data)
        # Convert linear magnitude to decibel scale
        audio.__magn_to_db(data)
        # Populate mapping variables for specified sampling policy
        audio.__fill_rfft_mapping()

    @staticmethod
    def __rfft_data(data):
        # Apply discrete fourier transform on windowed audio data & store as new key:value pair in dictionary
        # Parameters: data: [{'frame_data': string,
        #                     'frame_count': int,
        #                     'frame_time': float,
        #                     'frame_position': int,
        #                     'frame_decoded': type,
        #                     'frame_windowed': type}, ...]

        for i in range(len(data)):
            data[i]['frame_rfft'] = rfft(data[i]['frame_windowed'])

    @staticmethod
    def __magn_data(data):
        # Convert complex rfft coefficients to magnitude & store as new key:value pair in dictionary
        # Parameters: data: [{'frame_data': string,
        #                     'frame_count': int,
        #                     'frame_time': float,
        #                     'frame_position': int,
        #                     'frame_decoded': type,
        #                     'frame_windowed': type,
        #                     'frame_rfft': type}, ...]

        for i in range(len(data)):
            data[i]['frame_magn'] = abs(data[i]['frame_rfft'])

    @staticmethod
    def __magn_to_db(data):
        # Convert from linear magnitude to decibel scale in place & update corresponding 'frame_magn' value in dictionary
        # Parameters: data: [{'frame_data': string,
        #                     'frame_count': int,
        #                     'frame_time': float,
        #                     'frame_position': int,
        #                     'frame_decoded': type,
        #                     'frame_windowed': type,
        #                     'frame_rfft': type,
        #                     'frame_magn': type}, ...]

        for i in range(len(data)):
            data[i]['frame_magn'] = 20 * scipy.log10(data[i]['frame_magn'])


    @staticmethod
    def __fill_rfft_mapping():
        # Populate mapping variables with corresponding frequencies and bin indexes
        audio.__rfft_freq_index = []
        for i in range(config_audio.frames_per_buffer / 2):
            audio.__rfft_freq_index.append(int(round(i * config_audio.sampling_rate / float(config_audio.frames_per_buffer))))

        audio.__rfft_bin_index = []
        for i in range(config_audio.sampling_rate / 2 - config_audio.sampling_rate / config_audio.frames_per_buffer):
            audio.__rfft_bin_index.append(int(round(i * config_audio.frames_per_buffer / float(config_audio.sampling_rate))))


    @staticmethod
    def rfft_map_to_bin(freq):
        # Returns mapping from frequency to corresponding rfft bin index
        if 0 <= freq < len(audio.__rfft_bin_index):
            return audio.__rfft_bin_index[freq]

