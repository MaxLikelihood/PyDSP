from config import audio as config_audio
from config import analysis as config_analysis
import numpy as np
import scipy
from scipy import signal
from scipy.fftpack import rfft, rfftfreq

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
            data[i]['frame_decoded'] = np.fromstring(data[i]['frame_data'],
                                                        dtype = config_analysis.decoding_format,
                                                        count = data[i]['frame_count'])

    @staticmethod
    def __window_data(data):
        # Apply window function to the decoded data & store as new key:value pair in dictionary
        # Parameters: data: [{'frame_data': string,
        #                     'frame_count': int,
        #                     'frame_time': float,
        #                     'frame_position': int,
        #                     'frame_decoded': numpy.ndarray}, ...]

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
        #                     'frame_decoded': numpy.ndarray,
        #                     'frame_windowed': numpy.ndarray}, ...]

        for i in range(len(data)):
            data[i]['frame_rfft'] = rfft(data[i]['frame_windowed'])

    @staticmethod
    def __magn_data(data):
        # Convert complex rfft coefficients to magnitude & store as new key:value pair in dictionary
        # Parameters: data: [{'frame_data': string,
        #                     'frame_count': int,
        #                     'frame_time': float,
        #                     'frame_position': int,
        #                     'frame_decoded': numpy.ndarray,
        #                     'frame_windowed': numpy.ndarray,
        #                     'frame_rfft': numpy.ndarray}, ...]

        for i in range(len(data)):
            rfft_bin = np.append(0, data[i]['frame_rfft'])
            if data[i]['frame_rfft'].size % 2 == 0:
                rfft_bin = np.append(rfft_bin, 0)

            magnitude = []
            for j in range(0, rfft_bin.size, 2):
                magnitude.append(rfft_bin[j] * rfft_bin[j] + rfft_bin[j+1] * rfft_bin[j+1])

            data[i]['frame_magn'] = np.asarray(magnitude)

    @staticmethod
    def __magn_to_db(data):
        # Convert from linear magnitude to decibel scale in place & update corresponding 'frame_magn' value in dictionary
        # Parameters: data: [{'frame_data': string,
        #                     'frame_count': int,
        #                     'frame_time': float,
        #                     'frame_position': int,
        #                     'frame_decoded': numpy.ndarray,
        #                     'frame_windowed': numpy.ndarray,
        #                     'frame_rfft': numpy.ndarray,
        #                     'frame_magn': numpy.ndarray}, ...]

        for i in range(len(data)):
            data[i]['frame_magn'] = 20 * scipy.log10(data[i]['frame_magn'])


    @staticmethod
    def __fill_rfft_mapping():
        # Populate mapping variables with corresponding frequencies and bin indexes
        audio.__rfft_freq_index = []

        sample_frequencies = rfftfreq(config_audio.frames_per_buffer, 1 / float(config_audio.sampling_rate)).tolist()

        for i in range(len(sample_frequencies)):
            sample_frequencies[i] = int(round(sample_frequencies[i]))
            if sample_frequencies[i] not in audio.__rfft_freq_index:
                audio.__rfft_freq_index.append(sample_frequencies[i])

        audio.__rfft_bin_index = []

        for i in range(config_audio.sampling_rate / 2 + 1):
            audio.__rfft_bin_index.append(int(round(i * config_audio.frames_per_buffer / float(config_audio.sampling_rate))))


    @staticmethod
    def rfft_map_to_bin(freq):
        # Returns mapping from frequency to corresponding rfft bin index
        if 0 <= freq < len(audio.__rfft_bin_index):
            return audio.__rfft_bin_index[freq]


    @staticmethod
    def rfft_map_to_frequency(bin):
        # Returns mapping from rfft bin index to corresponding frequency
        if 0 <= bin < len(audio.__rfft_freq_index):
            return audio.__rfft_freq_index[bin]


