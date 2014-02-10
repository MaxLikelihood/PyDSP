#!/usr/bin/env python

#Basic imports
from ctypes import *
import sys
from time import sleep
import Tkinter as tk

#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, CurrentChangeEventArgs, StepperPositionChangeEventArgs, VelocityChangeEventArgs
from Phidgets.Devices.Stepper import Stepper


class StepperControl():

    stepper = object
    position = 0


    # used for connecting to the stepper motor
    @staticmethod
    def initialize():
        global stepper
        try:
            stepper = Stepper()
        except RuntimeError as e:
            print("Runtime Exception: %s" % e.details)
            print("Exiting....")
            exit(1)

        print("Opening phidget object....")

        try:
            stepper.openPhidget()
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Exiting....")
            exit(1)

        print("Waiting for attach....")

        try:
            stepper.waitForAttach(10000)
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            try:
                stepper.closePhidget()
            except PhidgetException as e:
                print("Phidget Exception %i: %s" % (e.code, e.details))
                print("Exiting....")
                exit(1)
            print("Exiting....")
            exit(1)
        else:
            pass

        try:
            print("Set the current position as start position...")
            stepper.setCurrentPosition(0, 0)
            sleep(1)

            print("Set the motor as engaged...")
            stepper.setEngaged(0, True)
            sleep(1)

            print("The motor will run until it reaches the set goal position...")

            stepper.setAcceleration(0, 4000)
            stepper.setVelocityLimit(0, 4000)
            stepper.setCurrentLimit(0, 0.26)

            sleep(2)

        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))
            print("Exiting....")
            exit(1)

        print("Initialized")

    # function is sued for calibrating the motor
    @staticmethod
    def stepper_move(pos):
        global stepper, position
        current = stepper.getCurrentPosition(0)
        target = current + pos
        print "target: ",target
        stepper.setTargetPosition(0, target)
        while(stepper.getCurrentPosition(0) != target):
            pass
        position = target


    @staticmethod
    def stepper_move_to(pos):
        global stepper
        stepper.setTargetPosition(0, pos)
        while(stepper.getCurrentPosition(0) != pos):
            pass

    # returns the current position of stepper motor
    @staticmethod
    def stepper_position():
        global stepper
        return stepper.getCurrentPosition(0)

    # moves the stepper to the start position
    @staticmethod
    def steppper_move_to_start():
        global stepper
        stepper.setTargetPosition(0, 0)
        while stepper.getCurrentPosition(0) != 0:
            pass

    # moves the stepper to the calibrated position
    @staticmethod
    def stepper_move_to_end():
        global stepper, position
        stepper.setTargetPosition(0, position)
        while stepper.getCurrentPosition(0) != position:
            pass

    # disenages the stepper motor
    @staticmethod
    def disengage():
        global stepper
        stepper.setEngaged(0, False)
        stepper.closePhidget()





