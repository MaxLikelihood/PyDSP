import pyaudio
import config
import time

class audio(object):

    active = False

    def instantiate(self):
        # instantiate PyAudio
        self.p = pyaudio.PyAudio()
        # locate host_api by name provided in config
        self.host_api_index = self.findHostAPI()
        if self.host_api_index == -1:
            print "\nInvalid Host API: %s" % config.host_api
        else:
            print "\nValid Host API: %s" % config.host_api
            # locate host_api_device by name provided in config
            self.host_api_device_index = self.findDevice()
            if self.host_api_device_index == -1:
                print "\nInvalid Host API Device: %s" % config.host_api_device
            else:
                print "\nValid Host API Device: %s" % config.host_api_device
                try:
                    self.supported = self.p.is_format_supported(rate = config.sampling_rate,
                                                                input_device = self.host_api_device_index,
                                                                input_channels = config.input_channels,
                                                                input_format = config.sampling_format,
                                                                output_device = None,
                                                                output_channels = None,
                                                                output_format = None)
                except ValueError as detail:
                    print "\nError Code: %d\nExplanation: %s" % (detail[1], detail[0])
                finally:
                    if self.supported == False:
                        print "\nInvalid Stream Parameters"
                    else:
                        print "\nConfiguration Valid"

    def terminate(self):
        # terminate PyAudio
        self.p.terminate()

    def findHostAPI(self):
        # locate the host api specified in config
        # return index if found, otherwise return -1
        host_api_count = self.p.get_host_api_count()
        if host_api_count <= 0:
            return -1
        else:
            for i in range(host_api_count):
                host_api_info = self.p.get_host_api_info_by_index(i)
                if host_api_info['name'] == config.host_api:
                    return i
            else:
                return -1

    def findDevice(self):
        # locate the device within the specified host api
        # return index if found, otherwise return -1
        self.host_api_device_count = self.p.get_host_api_info_by_index(self.host_api_index)['deviceCount']
        if self.host_api_device_count <= 0:
            return -1
        else:
            for i in range(self.host_api_device_count):
                device_info = self.p.get_device_info_by_host_api_device_index(self.host_api_index, i)
                if device_info['name'] == config.host_api_device:
                    return i
            else:
                return -1