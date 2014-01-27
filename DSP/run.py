from API import audio
from time import sleep

api = audio()

api.setup()

api.start_capture()

sleep(5)

api.stop_capture()

api.terminate()

