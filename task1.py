from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''


import numpy as np
import sys
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS)

RIGHT = BP.PORT_A
LEFT = BP.PORT_D

# Functions =======================================================

def turnRight(turnAmt):
    print("I turn right")
    y = 0 # has not turned yet
    first = BP.get_sensor(BP.PORT_3) # initial position
    while y != 1:
        sensorValues = BP.get_sensor(BP.PORT_3)
        if (sensorValues[0]) < (turnAmt+(first[0])):
            BP.set_motor_power(RIGHT, 20)
            BP.set_motor_power(LEFT, -20)  
        else:
            BP.set_motor_power(RIGHT, 0) 
            BP.set_motor_power(LEFT, 0) 
            y = 1
            time.sleep(0.025)
            
def turnLeft(turnAmt):
    print("I turn left")
    y = 0 # has not turned yet
    first = BP.get_sensor(BP.PORT_3) # initial position
    while y != 1:
        sensorValues = BP.get_sensor(BP.PORT_3)
        if (sensorValues[0]) > (first[0]-turnAmt):
            BP.set_motor_power(RIGHT, -20)
            BP.set_motor_power(LEFT, 20)  
        else:
            BP.set_motor_power(RIGHT, 0) 
            BP.set_motor_power(LEFT, 0) 
            y = 1
            time.sleep(0.025)

def goForward(amt):
    BP.set_motor_power(RIGHT, -30)
    BP.set_motor_power(LEFT, -30)
    time.sleep(amt)
    BP.set_motor_power(RIGHT, 0)
    BP.set_motor_power(LEFT, 0)
    print("I went forward once!")

# Logic =========================================

try:
    while True:
        turnAmt = int(input("Amt to turn: "))
        direction = input("r or l: ")
        if direction == 'r':
            turnRight(turnAmt)
        elif direction == 'l':
            turnLeft(turnAmt)
        #amt = float(input("time to test: "))
        #goForward(amt)
except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
    sys.exit()
