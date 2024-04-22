from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''


import numpy as np
import sys
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS)

RIGHT = BP.PORT_A
LEFT = BP.PORT_D
BACK = BP.PORT_B

# Functions =======================================================

def turnRight(turnAmt):
    print("I turn right")
    y = 0 # has not turned yet
    first = BP.get_sensor(BP.PORT_1) # initial position
    while y != 1:
        sensorValues = BP.get_sensor(BP.PORT_1)
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
    first = BP.get_sensor(BP.PORT_1) # initial position
    while y != 1:
        sensorValues = BP.get_sensor(BP.PORT_1)
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

def dropCargo(num):
    BP.set_motor_power(BACK, num)
    time.sleep(1)
    BP.set_motor_power(BACK, 0)
    time.sleep(1)
    print("I dropped a shit!")
    

# Logic =========================================

try:
    try:
        while True:
            option = input("t or c: ")
            if option == "t":
                turnAmt = int(input("Amt to turn: "))
                direction = input("r or l or : ")
                if direction == 'r':
                    turnRight(turnAmt)
                elif direction == 'l':
                    turnLeft(turnAmt)
            elif option == "c":
                num = int(input("cargo speed test number: "))
                dropCargo(num)
            #amt = float(input("time to test: "))
            #goForward(amt)
    except brickpi3.SensorError as error:
        print(error)     
except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
    sys.exit()
