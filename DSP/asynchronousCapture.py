import matplotlib.pyplot
import pyaudio
import numpy
import scipy
import time
import sys


# define callback function
def callback(in_data, frame_count, time_info, status_flags):
    return (None, pyaudio.paContinue)

# instantiate PortAudio
p = pyaudio.PyAudio()

# get default Host API
default_host_api = p.get_default_host_api_info()

print "Default Host API: %s\n" % default_host_api['name']

# list default Host API input devices if available
if default_host_api['deviceCount'] != pyaudio.paNoDevice:
    input_devices = []
    print "Index\t Name"
    for i in range(default_host_api['deviceCount']):
        device_info = p.get_device_info_by_host_api_device_index(default_host_api['index'], i)
        if device_info['maxInputChannels'] != 0L:
            print "%d\t %s" % (device_info['index'], device_info['name'])
            input_devices.append(device_info['index'])
    else:
        if len(input_devices) == 0:
            print "No Input Devices Available"
        else:
            print "\n%d Input Devices Found\n" % (len(input_devices))

selected_input = raw_input("Select by index: ")

if int(selected_input) not in input_devices:
    print "Invalid selection"
    p.terminate()
    sys.exit(1)
else:
    selected_input = p.get_device_info_by_host_api_device_index(default_host_api['index'], int(selected_input))
    print "\nSelection: %s" % selected_input['name']
    print "MaxInputChannels: %d" % selected_input['maxInputChannels']
    print "DefaultLowInputLatency: %f" % selected_input['defaultLowInputLatency']
    print "DefaultHighInputLatency: %f" % selected_input['defaultHighInputLatency']

supported = False

while supported == False:
    input_sampling_rate = int(raw_input("\nSampling rate (Hz): "))
    input_input_channel = int(raw_input("Number of input channels: "))

    try:
        supported = p.is_format_supported(rate = input_sampling_rate,
                                          input_device = selected_input['index'],
                                          input_channels = input_input_channel,
                                          input_format = pyaudio.paFloat32,
                                          output_device = None,
                                          output_channels = None,
                                          output_format = None)
    except ValueError as detail:
        print "\nError Code: %d\nExplanation: %s" % (detail[1], detail[0])
    finally:
        if supported == False:
            print "\nTry again"

print "\nFormat supported"

stream = p.open(rate = input_sampling_rate,
                channels = input_input_channel,
                format = pyaudio.paFloat32,
                input = True,
                output = False,
                input_device_index = selected_input['index'],
                output_device_index = None,
                frames_per_buffer = 1024,
                start = False,
                stream_callback = callback)


print "\nStarting Stream"
stream.start_stream()

time.sleep(1)

print "\nClosing Stream"
stream.close()

p.terminate()
