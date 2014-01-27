import pyaudio
import config
import time

class audioAPI(object):

    def instantiate(self):
        # instantiate PyAudio
        self.p = pyaudio.PyAudio()
        self.host_api_index = self.findHostAPI()
        


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
