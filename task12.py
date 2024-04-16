
from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division  
import os

# Set the MPLCONFIGDIR environment variable to a writable directory
os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib_config'

import numpy as np
import matplotlib.pyplot as p
import sys
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import grovepi


BP = brickpi3.BrickPi3() 
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS) # gyro sensor
RIGHT = BP.PORT_A
LEFT = BP.PORT_D
BACK = BP.PORT_B

# Functions =======================================================

def turnRight(pos):
    if (pos == 'up'):
        pos = 'right'
    elif (pos == 'left'):
        pos = 'up'
    elif (pos == 'down'):
        pos = 'left'
    elif (pos == 'right'):
        pos = 'down'
    print("I turn left")
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
    return pos
            
def turnLeft(pos):
    if (pos == 'up'):
        pos = 'left'
    elif (pos == 'left'):
        pos = 'down'
    elif (pos == 'down'):
        pos = 'right'
    elif (pos == 'right'):
        pos = 'up'
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
    return(pos)

def goForward():
    BP.set_motor_power(RIGHT, -30)
    BP.set_motor_power(LEFT, -30)
    time.sleep(0.3)
    #BP.set_motor_power(RIGHT, 0)
    #BP.set_motor_power(LEFT, 0)
    
    print("I went forward once!")

def dropCargo():
    BP.set_motor_power(BACK, 15)
    time.sleep(1)
    BP.set_motor_power(BACK, 0)
    time.sleep(1)
    BP.set_motor_power(BACK, -15)
    time.sleep(0.5)
    BP.set_motor_power(BACK, 0)
    print("I dropped a shit!")
    
    
# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")
BP = brickpi3.BrickPi3() 

# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND

front = 8
left = 3 # left
#right = 2 # right

# Variables =====================================================

ft = 10 # front threshold
speed = int(input("desired speed for testing: "))
x = 1
cpx = 0
cpy = 0

pos = "up"
place = [[0]]

xMax = 0
yMax = 0

# Logic =========================================================

try:
    while True:
        usf = grovepi.ultrasonicRead(front)
        usl = grovepi.ultrasonicRead(left)
        #usr = grovepi.ultrasonicRead(right)
        print(f"f: {usf}, l: {usl}")
        if (usf < ft):
            if (usl > 40):
                pos = turnLeft(pos)
            else:
                pos = turnRight(pos)
        else:
            goForward()
            if (pos == 'up'):
                cpy += 1
                place.append([])
                for i in range(0, cpx, 1):
                    place[cpy].append(1)
                place[cpy].append(0)    
            elif (pos == 'right'):
                cpx += 1
                place[cpy].append(0)
                for i in range(0, len(place), 1):
                    if (i != cpy):
                        place[i].append(1) 
            elif (pos == 'left'):
                cpx -= 1
                place[cpy][cpx] = 0 
            elif (pos == 'down'):
                cpy -= 1
                place[cpy][cpx] = 0 
            if (cpx > xMax):
                xMax = cpx    
            if (cpy > yMax):
                yMax = cpy                  
        time.sleep(0)

    
      
except KeyboardInterrupt:
    BP.set_motor_power(RIGHT, 0)
    BP.set_motor_power(LEFT, 0)
    time.sleep(0.5)
    dropCargo()
    print(place)
    Xaxis = np.linspace(0,xMax,1)
    Yaxis = np.linspace(0,yMax,1)
    [X,Y] = np.meshgrid(Xaxis, Yaxis)
    
    place = np.transpose(place) # flip??
    place = np.rot90(place, 1, (0,1)) # rotate???
    p.imshow(place, cmap = 'YlGnBu_r', interpolation = 'nearest') 
    p.show() 
    print("ctrl + c")
    BP.reset_all()
    sys.exit
