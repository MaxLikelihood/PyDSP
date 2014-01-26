Digital Signal Processing (DSP) Codeblocks
=============================================
queryHostAPI
---------------------------------------------
Perform standard query on all available Host APIs, displays:

    Host API Name
    Number of Devices associated to Host API 
    Default Input/Output Devices for Host API if available

asynchronousCapture
---------------------------------------------
Framework for asynchronous (callback) capture through PyAudio. Abstract callback function protoype is provided.
Defaults Include:

    Default Host API
    Default Sample Format as paFloat32
    
User Parameters Include:

    Input Device Selection
    Recording Channels Specification
    Recording Sample Rate Specification
    
