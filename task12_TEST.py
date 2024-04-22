
from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division  
import os

# Set the MPLCONFIGDIR environment variable to a writable directory
os.environ['MPLCONFIGDIR'] = '/tmp/matplotlib_config'
from MPU9250 import MPU9250
import numpy as np
import matplotlib.pyplot as p
import matplotlib.patches as pp
import sys
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import grovepi

print("beep boop. initializing!")
BP = brickpi3.BrickPi3() 
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS) # gyro sensor
RIGHT = BP.PORT_A
LEFT = BP.PORT_D
BACK = BP.PORT_B
mpu9250 = MPU9250()

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
    try:
        first = BP.get_sensor(BP.PORT_1) # initial position
        while y != 1:
            sensorValues = BP.get_sensor(BP.PORT_1)
            if (sensorValues[0]) < (84+(first[0])):
                BP.set_motor_power(RIGHT, 20)
                BP.set_motor_power(LEFT, -20)  
            else:
                BP.set_motor_power(RIGHT, 0) 
                BP.set_motor_power(LEFT, 0) 
                y = 1
                time.sleep(0.025)
        time.sleep(0.2)
    except brickpi3.SensorError as error:
        print(error)
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
    try:
        first = BP.get_sensor(BP.PORT_1) # initial position
        while y != 1:
            sensorValues = BP.get_sensor(BP.PORT_1)
            if (sensorValues[0]) > (first[0]-84):
                BP.set_motor_power(RIGHT, -20)
                BP.set_motor_power(LEFT, 20)  
            else:
                BP.set_motor_power(RIGHT, 0) 
                BP.set_motor_power(LEFT, 0) 
                y = 1
                time.sleep(0.025)
        time.sleep(0.2)
    except brickpi3.SensorError as error:
        print(error)    
    return(pos)

def goForward():
    BP.set_motor_power(RIGHT, -15)
    BP.set_motor_power(LEFT, -15)
    time.sleep(0.3)
    #BP.set_motor_power(RIGHT, 0)
    #BP.set_motor_power(LEFT, 0)
    
    print("I went forward once!")

def dropCargo():
    BP.set_motor_power(BACK, 40)
    time.sleep(1)
    BP.set_motor_power(BACK, 0)
    time.sleep(1)
    print("I dropped a shit!")
    
# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")
BP = brickpi3.BrickPi3() 

# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND

front = 8
left = 3 # left
#right = 2 # right

one = 14		# Pin 14 is A0 Port.
two = 15		# Pin 15 is A0 Port.     
grovepi.pinMode(one,"INPUT")
grovepi.pinMode(two,"INPUT")           

# Variables =====================================================

ft = 5 # front threshold
lt = 20 # left threshold

x = 1
cpx = 35
cpy = 20

pos = "right"
place = [ 
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
         [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0.3]
        ]

xMax = cpx
yMax = cpy

irmax = 72 # value we will decide
magmax = 100 # value we will decide

irobst_y = 0
irobst_x = 0
magobst_x = 0
magobst_y = 0

fid = open("team35_hazards.csv","w")

fid.write("Team: 35\nHazard Type, Parameter of Interest, Parameter Value, Hazard X Coordinate (cm), Hazard Y Coordinate (cm)")


# fid.write("\nHigh Temperature Heat Source, Radiated Power (W)" + str(irmax) + ", " + str(irobst_x * 3.75) + ", " + str(irobst_y * 3.75))


# Logic =========================================================
start = input("PRESS ENTER TO START!")

try:
    while True:
        usf = grovepi.ultrasonicRead(front)
        usl = grovepi.ultrasonicRead(left)
        irone  = grovepi.analogRead(one)
        irtwo = grovepi.analogRead(two)
        
        mag_x = mpu9250.readMagnet()['x']
        #print(mag_x)
        irreal = 0.5 * (irone + irtwo)
        print(irreal)
        #usr = grovepi.ultrasonicRead(right)
        print(f"f: {usf}, l: {usl}")
        if (usf < ft):
            if (usl > lt):
                pos = turnLeft(pos)
            else:
                pos = turnRight(pos)
        elif (irreal > irmax):
            print("IR READ")
            if (pos == 'up'):
                irobst_y = cpy + 2
                irobst_x = cpx
                
                print(len(place))
                place.append([])
                for i in range(0, xMax + 1, 1):
                    place[cpy + 1].append(1)
                print(len(place))    
                place.append([])
                for i in range(0, xMax + 1, 1):
                    place[irobst_y].append(1)
                print(len(place))
                print(len(place[irobst_y]))
                print(f'y: {irobst_y} x: {irobst_x}')  
                                  
                place[irobst_y][cpx] = 0.8
                if (irobst_y > yMax):
                    yMax = irobst_y              
                
            elif (pos == 'left'):
                irobst_x = cpx - 2
                irobst_y = cpy

                place[irobst_y][irobst_x] = 0.8 
                
            elif (pos == 'right'):
                irobst_x = cpx + 2
                irobst_y = cpy     

                if ((irobst_x) > (len(place[cpy]))): 
                    place[cpy].append(1)
                    place[cpy].append(1)
                    for i in range(0, len(place), 1):
                        if (i != cpy):
                            place[i].append(1)
                            place[i].append(1)
                else:
                    place[cpy][cpx+1] = 1
                place[cpy][irobst_x] = 0.8 
                if (irobst_x > xMax):
                    xMax = irobst_x        
                                     
            
            elif (pos == 'down'):
                irobst_x = cpx 
                irobst_y = cpy - 2
                
                place[irobst_y][irobst_x] = 0.8                
            fid = open("team35_hazards.csv","a")   
            fid.write("\nHigh Temperature Heat Source, Radiated Power (W)" + str(irmax) + ", " + str(irobst_x * 3.75) + ", " + str(irobst_y * 3.75))
            fid.close()
            
            if (usl > lt):
                pos = turnLeft(pos)
            else:
                pos = turnRight(pos)       
                                   
        elif (mag_x > magmax):
            if (pos == 'up'):
                magobst_y = cpy + 2
                magobst_x = cpx
                
                print(len(place))
                place.append([])
                for i in range(0, xMax + 1, 1):
                    place[cpy + 1].append(1)
                print(len(place))    
                place.append([])
                for i in range(0, xMax + 1, 1):
                    place[magobst_y].append(1)
                #print(len(place))
                #print(len(place[magobst_y]))
                #print(f'y: {magobst_y} x: {magobst_x}')  
                                  
                place[magobst_y][cpx] = 0.7
                if (magobst_y > yMax):
                    yMax = magobst_y  
                    
                                
            elif (pos == 'left'):
                magobst_x = cpx - 2
                magobst_y = cpy

                place[magobst_y][magobst_x] = 0.7 
                
            elif (pos == 'right'):
                magobst_x = cpx + 2
                magobst_y = cpy     

                if ((magobst_x) > (len(place[cpy]))): 
                    place[cpy].append(1)
                    place[cpy].append(1)
                    for i in range(0, len(place), 1):
                        if (i != cpy):
                            place[i].append(1)
                            place[i].append(1)
                else:
                    place[cpy][cpx+1] = 1
                place[cpy][magobst_x] = 0.7 
                if (magobst_x > xMax):
                    xMax = magobst_x        
                                
            elif (pos == 'down'):
                magobst_x = cpx 
                magobst_y = cpy - 2
                
                place[magobst_y][magobst_x] = 0.7 
            fid = open("team35_hazards.csv","a")    
            fid.write("\nElectrical/Magnetic Activity Source, Field Strength (uT)," + str(magmax) + ", " + str(magobst_x * 3.75) + ", " + str(magobst_y * 3.75))
            fid.close()                                                                 
            if (usl > lt):
                pos = turnLeft(pos)
            else:
                pos = turnRight(pos)  
                      
        else:
            goForward()
            if (pos == 'up'):
                cpy += 1
                place.append([])
                if (cpx == xMax):
                    for i in range(0, cpx, 1):
                        place[cpy].append(1)
                    place[cpy].append(0)
                else:
                    print(f"xmax: {xMax}; ymax: {yMax}")
                    print("I am here")
                    #for i in range(0, xMax, 1):
                        #place[cpy].append(1)
                        #print("I HAVE ARRIVED")

                    for i in range(0, len(place), 1):
                        if (len(place[i]) == 0):
                            for f in range(0, xMax + 1, 1):
                                place[i].append(1)
                        print(f"length of {len(place[i])}")            
                    place[cpy][cpx]= 0
                    #place[cpy].append(1)
                                      
                
            elif (pos == 'right'):
                cpx += 1
                if ((cpx + 1) > len(place[cpy])): 
                    place[cpy].append(0)
                    for i in range(0, len(place), 1):
                        if (i != cpy):
                            place[i].append(1)
                else:
                    place[cpy][cpx] = 0  
                    
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
    if (place[-1] == []):
        place.pop()
    BP.set_motor_power(RIGHT, 0)
    BP.set_motor_power(LEFT, 0)

    print(cpx)
    print(cpy)
    print("===")
    #print(len(place[0]))
    #print(len(place))
    print(cpy - 20)
    place[cpy][cpx] = 0.5
    
    time.sleep(0.5)
    dropCargo()
    print(place)
    Xaxis = np.linspace(0,xMax,1)
    Yaxis = np.linspace(0,yMax,1)
    [X,Y] = np.meshgrid(Xaxis, Yaxis)
    
    place = np.transpose(place) # flip??
    place = np.rot90(place, 1, (0,1)) # rotate???
    p.imshow(place, cmap = 'YlGnBu_r', interpolation = 'nearest')
    
    start_patch =  pp.Patch(color = '#225ea8', label = 'Origin')
    path_patch = pp.Patch(color = '#081d58', label = 'Path GEARS took')
    end_patch = pp.Patch(color = '#7fcdbb', label = 'Exit Point')
    the_rest = pp.Patch(color = '#ffffd9', label = 'Not part of path')
    irobst = pp.Patch(color = '#edf8b1', label = 'Heat Source')
    magobst = pp.Patch(color = '#c7e9b4', label = 'Magnetic Source')
    
    p.legend(handles = [start_patch, path_patch, end_patch, the_rest, irobst, magobst],loc='lower left')
    p.show() 

    fid.close()
    
    print("ctrl + c")
    BP.reset_all()
    sys.exit
