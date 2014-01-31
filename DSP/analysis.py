from config import audio as config_audio
import numpy
import scipy

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


    