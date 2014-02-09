from API import audio
from time import sleep
from analysis import audio as analysis_audio
from plot import plotter
from stepperControl import StepperControl

StepperControl.initialize()

api = audio()

api.setup()

a = 1
while( int(a) != 0):
    a = raw_input()
    StepperControl.stepper_move(int(a))

StepperControl.steppper_move_to_start()
api.start_capture()

#sleep(10)
StepperControl.stepper_move_to_end()

api.stop_capture()

data = api.get_data()

analysis_audio.analyze(data)

plotter.generate_plot_for_frequency(data, 'frame_position', 'frame_magn', 18000)

StepperControl.stepper_move_to(analysis_audio.find_max_of_respect_to_for_frequency(data, 'frame_magn', 'frame_position', 18000))

plotter.generate_plot_for_frequency(data, 'frame_position', 'frame_magn', 19000)

StepperControl.stepper_move_to(analysis_audio.find_max_of_respect_to_for_frequency(data, 'frame_magn', 'frame_position', 19000))

api.destroy()

StepperControl.disengage()
