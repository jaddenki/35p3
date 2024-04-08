from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import numpy as np
import sys
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import grovepi

BP = brickpi3.BrickPi3() 
RIGHT = BP.PORT_A
LEFT = BP.PORT_D

# Functions =======================================================

def turnRight():
    print("I turn right")
    y = 0 # has not turned yet
    first = BP.get_sensor(BP.PORT_3) # initial position
    while y != 1:
        sensorValues = BP.get_sensor(BP.PORT_3)
        if (sensorValues[0]) < (84+(first[0])):
            BP.set_motor_power(RIGHT, 20)
            BP.set_motor_power(LEFT, -20)  
        else:
            BP.set_motor_power(RIGHT, 0) 
            BP.set_motor_power(LEFT, 0) 
            y = 1
            time.sleep(0.025)
    time.sleep(0.2)
            
def turnLeft():
    print("I turn left")
    y = 0 # has not turned yet
    first = BP.get_sensor(BP.PORT_3) # initial position
    while y != 1:
        sensorValues = BP.get_sensor(BP.PORT_3)
        if (sensorValues[0]) > (first[0]-84):
            BP.set_motor_power(RIGHT, -20)
            BP.set_motor_power(LEFT, 20)  
        else:
            BP.set_motor_power(RIGHT, 0) 
            BP.set_motor_power(LEFT, 0) 
            y = 1
            time.sleep(0.025)
    time.sleep(0.2)

# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")
BP = brickpi3.BrickPi3() 

# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND

front = 8
left = 3 # left
right = 2 # right

# Variables =====================================================

#ft = 5 # front threshold
#speed = int(input("desired speed for testing: "))
#x = 1

# Logic =========================================================

try:
    while True:
        try:    
            usf = grovepi.ultrasonicRead(front)
            usl = grovepi.ultrasonicRead(left)
            usr = grovepi.ultrasonicRead(right)
            print(f"f: {usf}, l: {usl}, r: {usr}")
            time.sleep(0.1)
        except brickpi3.SensorError as error:
            print(error)
        time.sleep(0.1)
        
except KeyboardInterrupt:
    print("ctrl + c")
    BP.reset_all()
    sys.exit
