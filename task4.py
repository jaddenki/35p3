from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       

import numpy as np
import sys
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import grovepi

BP = brickpi3.BrickPi3() 
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS) # gyro sensor


RIGHT = BP.PORT_A
LEFT = BP.PORT_D

# Functions =======================================================

def turnRight():
    print("I turn right")
    y = 0 # has not turned yet
    first = BP.get_sensor(BP.PORT_3) # initial position
    while y != 1:
        sensorValues = BP.get_sensor(BP.PORT_3)
        if (sensorValues[0]) < (87+(first[0])):
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
        if (sensorValues[0]) > (first[0]-87):
            BP.set_motor_power(RIGHT, -20)
            BP.set_motor_power(LEFT, 20)  
        else:
            BP.set_motor_power(RIGHT, 0) 
            BP.set_motor_power(LEFT, 0) 
            y = 1
            time.sleep(0.025)
    time.sleep(0.2)

def goForward():
    BP.set_motor_power(RIGHT, -30)
    BP.set_motor_power(LEFT, -30)
    time.sleep(1.65)
    BP.set_motor_power(RIGHT, 0)
    BP.set_motor_power(LEFT, 0)
    print("I went forward once!")
    time.sleep(0.2)
            
# Variables ==================================================

cpx = int(input("current point x: "))
cpy = int(input("current point y: "))
print("~~~~~~~~~~~~~~~~")
wpx = int(input("wanted point x: "))
wpy = int(input("wanted point y: "))
x = 1
pos = input("current orientation (left, right, up, down): ")

# Logic =====================================================

time.sleep(4)
try:
    while (x == 1):
        if ((cpx == wpx) and (cpy == wpy)):
            x = 0
        else:
            while (cpx != wpx):
                print(f"({cpx}, {cpy})") 
                if (cpx < wpx):
                    if (pos == 'up'):
                        turnRight()
                        pos = 'right'
                    elif (pos == 'left'):
                        turnLeft()
                        turnLeft()
                        pos = 'right'
                    elif (pos == 'down'):
                        turnLeft()
                        pos = 'right'
                    goForward()
                    cpx += 1
                elif (cpx > wpx):
                    if (pos == 'right'):
                        turnLeft()
                        turnLeft()
                        pos = 'left'
                    elif (pos == 'up'):
                        turnLeft()
                        pos = 'left'
                    elif (pos == 'down'):
                        turnRight()
                        pos = 'left'
                    goForward()
                    cpx -= 1
            while (cpy != wpy):
                print(f"({cpx}, {cpy})") 
                if (cpy < wpy):
                    if (pos == 'right'):
                        turnLeft()
                        pos = 'up'
                    elif (pos == 'left'):
                        turnRight()
                        pos = 'up'
                    elif (pos == 'down'):
                        turnLeft()
                        turnLeft()
                        pos = 'up'
                    goForward()
                    cpy += 1
                elif (cpy > wpy):
                    if (pos == 'right'):
                        turnRight()
                        pos = 'down'
                    elif (pos == 'up'):
                        turnLeft()
                        turnLeft()
                        pos = 'down'
                    elif (pos == 'left'):
                        turnLeft()
                        pos = 'down'
                    goForward()
                    cpy -= 1
            
                        
except KeyboardInterrupt:
    print("u pressed ctrl + c")
    BP.reset_all()
    sys.exit