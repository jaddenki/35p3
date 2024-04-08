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
            
# Variables ==================================================

cpx = 0
cpy = 0

wpx = int(input("wpx: "))
wpy = int(input("wpy: "))

ob1x = int(input("ob1x: "))
ob1y = int(input("ob1y: "))

ob2x = int(input("ob2x: "))
ob2y =  int(input("ob2y: "))

x = 1 # true
pos = 'right'

# Logic =====================================================

time.sleep(4)
try:
    while (x == 1):
        if ((cpx == wpx) and (cpy == wpy)):
            x = 0
        else:
            
            while (cpx != wpx):
                print(f'({cpx}, {cpy})')
                time.sleep(1)
                if (((cpx + 1) == ob1x) and (cpy == ob1y)) or (((cpx + 1) == ob2x) and (cpy == ob2y)):
                    turnLeft()
                    goForward()
                    cpy += 1
                    turnRight()
                elif (cpx > wpx):
                    if (pos == 'up'):
                        turnLeft()
                        pos = 'left'
                        goForward()
                        cpx -= 1
                    elif (pos == 'right') and ((cpy + 1 != ob1y ) or (cpy + 1 != ob2y)):
                        turnLeft()
                        pos = 'up'
                        goForward()
                        cpy += 1
                    else:
                        turnLeft()
                        turnLeft()
                        pos = 'left'
                        goForward()
                        cpx -= 1
                else:
                    if (pos == 'up'):
                        turnRight()
                        pos = 'right'
                        goForward()
                        cpx += 1
                    else:
                        goForward()
                        cpx += 1
                        
            while (cpy != wpy):
                print(pos)
                print(f'({cpx}, {cpy})')
                time.sleep(1)
                if (((cpy + 1) == ob1y) and (cpx == ob1x)) or ((cpy + 1) == ob2y and (cpx == ob2x)):
                    if (cpx == 3):
                        turnLeft()
                        turnLeft()
                        goForward()
                        cpx -= 1
                        turnRight()
                        goForward()
                        pos = 'up'
                    elif (cpx == 0):
                        if (pos == 'up'):
                            print("im where i should be")
                            turnRight()
                            pos = 'right'
                        goForward()
                        cpx += 1
                    else:
                        if (cpx == 0) and (cpy == 0):
                            print("im hereeee")
                            turnLeft()
                            pos = 'up'
                        print("im here")
                        turnRight()
                        pos = 'right'
                        goForward()
                        cpx += 1
                else:
                    if (pos == 'right'):
                        print("am i here")
                        turnLeft()
                        pos = 'up'
                    print("I am here")    
                    goForward()
                    cpy += 1
                        
except KeyboardInterrupt:
    print("u pressed ctrl + c")
    BP.reset_all()
    sys.exit
