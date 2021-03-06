from config import audio as config_audio
import pyaudio
import time

class audio(object):

    # indicate stream active/inactive
    __active = False
    # indicate PyAudio instantiation status
    __instantiate = False

    # audio data represented as a list of dictionaries
    __data = []

    def setup(self):
        if audio.__instantiate:
            # avoid duplicated invocation
            return
        # instantiate PyAudio
        self.p = pyaudio.PyAudio()
        # locate host_api by name provided in config
        self.host_api_index = self.__findHostAPI()
        if self.host_api_index == -1:
            # specified host_api in config is unavailable
            print "\nInvalid Host API: %s" % config_audio.host_api
            self.p.terminate()
        else:
            print "\nValid Host API: %s" % config_audio.host_api
            # locate host_api_device by name provided in config
            self.host_api_device_index = self.__findDevice()
            if self.host_api_device_index == -1:
                # specified host_api_device in config is unavailable under host_api
                print "\nInvalid Host API Device: %s" % config_audio.host_api_device
                self.p.terminate()
            else:
                print "\nValid Host API Device: %s" % config_audio.host_api_device
                try:
                    self.supported = self.p.is_format_supported(rate = config_audio.sampling_rate,
                                                                input_device = self.host_api_device_index,
                                                                input_channels = config_audio.input_channels,
                                                                input_format = config_audio.sampling_format,
                                                                output_device = None,
                                                                output_channels = None,
                                                                output_format = None)
                except ValueError as detail:
                    print "\nError Code: %d\nExplanation: %s" % (detail[1], detail[0])
                finally:
                    if self.supported:
                        print "\nConfiguration Valid"
                        audio.__instantiate = True
                    else:
                        # specified audio stream parameters are not compatible
                        print "\nInvalid Stream Parameters"
                        self.p.terminate()

    def destroy(self):
        if not audio.__instantiate:
            return
        # close active stream before termination
        self.__close_stream()
        # terminate PyAudio
        self.p.terminate()
        audio.__instantiate = False

    def __findHostAPI(self):
        # locate the host api specified in config
        # return index if found, otherwise return -1
        host_api_count = self.p.get_host_api_count()
        if host_api_count <= 0:
            return -1
        else:
            for i in range(host_api_count):
                host_api_info = self.p.get_host_api_info_by_index(i)
                if host_api_info['name'] == config_audio.host_api:
                    return i
            else:
                return -1

    def __findDevice(self):
        # locate the device within the specified host api
        # return index if found, otherwise return -1
        self.host_api_device_count = self.p.get_host_api_info_by_index(self.host_api_index)['deviceCount']
        if self.host_api_device_count <= 0:
            return -1
        else:
            for i in range(self.host_api_device_count):
                device_info = self.p.get_device_info_by_host_api_device_index(self.host_api_index, i)
                if device_info['name'] == config_audio.host_api_device:
                    return i
            else:
                return -1

    # define callback function
    def __callback(self, in_data, frame_count, time_info, status_flags):
        audio.__data.append({'frame_data': in_data,
                             'frame_count': frame_count,
                             'frame_time': time.time() - audio.__time,
                             'frame_position': 0 }) # stepper motor position
        return (None, pyaudio.paContinue)

    def __start_stream(self):
        if audio.__active:
            # prevent duplicated stream opening
            return
        else:
            audio.stream = self.p.open(rate = config_audio.sampling_rate,
                                       channels = config_audio.input_channels,
                                       format = config_audio.sampling_format,
                                       input = True,
                                       output = False,
                                       input_device_index = self.host_api_device_index,
                                       output_device_index = None,
                                       frames_per_buffer = config_audio.frames_per_buffer,
                                       start = True,
                                       stream_callback = self.__callback)
            audio.__active = True
            audio.__time = time.time()

    def __close_stream(self):
        if not audio.__active:
            # prevent duplicated stream closing
            return
        else:
            audio.stream.close()
            audio.__active = False

    def start_capture(self):
        if audio.__instantiate:
            self.__start_stream()

    def stop_capture(self):
        if audio.__instantiate:
            self.__close_stream()

    def get_data(self):
        return audio.__data

    def get_data_length(self):
        return len(audio.__data)

    def clear_data(self):
        audio.__data = []