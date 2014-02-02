from API import audio
from time import sleep
from analysis import audio as analysis_audio
from plot import plotter


api = audio()

api.setup()

api.start_capture()

sleep(10)

api.stop_capture()

data = api.get_data()

analysis_audio.analyze(data)

plotter.generate_plot_for_frequency(data, 'frame_time', 'frame_magn', 18000)

api.destroy()

