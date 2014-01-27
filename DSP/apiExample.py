# module import
from API import audio
from time import sleep

# instantiate audio api object
api = audio()

# setup api object for further interaction
api.setup()

# begin audio capture into audio data, using specified parameters in config.py
api.start_capture()

# capture for 5 seconds
sleep(5)

# stop audio capture   
api.stop_capture()

# display captured audio data length
print api.get_data_length()

# begin audio capture into audio data, appending to existing audio data
api.start_capture()

# capture for 5 seconds
sleep(5)

# stop audio capture
api.stop_capture()

# display captured audio data length, notice the length should be approximately doubled
print api.get_data_length()

# clear captured audio data
api.clear_data()

# display captured audio data length
print api.get_data_length() #prints 0

# destroy api object, no further interaction allowed unless setup() is called again
api.destroy()