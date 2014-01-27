Digital Signal Processing (DSP) Codeblocks
=============================================
API.py
---------------------------------------------
API wrapper for [PyAudio][1], providing simplified user-interface and integration with `config.py`. Available functionalities include:

-   `setup()` - initialize the API object, required before any further interaction
-   `destroy()` - destroy the API object, previously initialized through  `setup()`, no further interaction allowed
-   `start_capture()` - begin audio capture into audio data
-   `stop_capture()` - stop audio capture
-   `get_data()` - retrieve captured audio data
-   `get_data_length()` - retrieve length of captured audio data
-   `clear_data()` - clear captured audio data, possibly for fresh capture

Captured audio data has the following type:

`[{'frame_data': string, 'frame_count': int, 'frame_time': float, 'frame_position': int}, ... ]`

For example usage, see `apiExample.py`

config.py
---------------------------------------------
Configuration file for project

Audio Configuration:

    host_api
    host_api_device
    sampling_rate
    input_channels
    sampling_format
    frames_per_buffer
    

queryHostAPI.py
---------------------------------------------
Perform standard query on all available Host APIs, displays:

    Host API Name
    Number of Devices associated to Host API 
    Default Input/Output Devices for Host API if available

asynchronousCapture.py
---------------------------------------------
Framework for asynchronous (callback) capture through PyAudio. Abstract callback function protoype is provided.
Defaults Include:

    Default Host API
    Default Sample Format as paFloat32
    
User Parameters Include:

    Input Device Selection
    Recording Channels Specification
    Recording Sample Rate Specification
    
[1]: http://people.csail.mit.edu/hubert/pyaudio/ "PyAudio Mainpage"
