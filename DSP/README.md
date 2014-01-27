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

Example Usage:

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
