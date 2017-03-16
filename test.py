# -*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
from robotcontrol import Robot, Motor
from sonar import Sonar

GPIO.setmode(GPIO.BCM)

robot = Robot()

while 1:
        #try:
                robot.set_angle(100)
                robot.set_speed(80)
                robot.compute_and_go()
        #except:
        #        break

robot.stop()

GPIO.cleanup()
print("--- Fin du programme ---")