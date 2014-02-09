from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, CurrentChangeEventArgs, StepperPositionChangeEventArgs, VelocityChangeEventArgs
from Phidgets.Devices.Stepper import Stepper as Phidgets_stepper
from config import stepper as config_stepper
from time import sleep

class stepper(object):

    # indicate device attachment status
    __attachment = False

    # indicate device active position
    __active_position = 0

    # indicate device virtual position
    __virtual_position = 0

