import pyaudio
import numpy
import scipy

p = pyaudio.PyAudio()

host_api_count = p.get_host_api_count()

print "Number of available Host API: %d" % host_api_count

for i in range(host_api_count):
    host_api = p.get_host_api_info_by_index (i)
    if host_api['deviceCount'] != pyaudio.paNoDevice:
        if 'defaultOutputDevice' in host_api and 'defaultInputDevice' in host_api:
            print "Name: %s\t Device Count: %d\t Default Output: %s\t Default Input: %s" % (host_api['name'], host_api['deviceCount'], p.get_device_info_by_host_api_device_index(i, host_api['defaultOutputDevice'])['name'] , p.get_device_info_by_host_api_device_index(i, host_api['defaultInputDevice'])['name'])
        elif 'defaultOutputDevice' in host_api:
            print "Name: %s\t Device Count: %d\t Default Output: %s" % (host_api['name'], host_api['deviceCount'], p.get_device_info_by_host_api_device_index(i, host_api['defaultOutputDevice'])['name'])
        elif 'defaultInputDevice' in host_api:
            print "Name: %s\t Device Count: %d\t Default Input: %s" % (host_api['name'], host_api['deviceCount'], p.get_device_info_by_host_api_device_index(i, host_api['defaultInputDevice'])['name'])
        else:
            print "Name: %s\t Device Count: %d" % (host_api['name'], host_api['deviceCount'])

p.terminate()
