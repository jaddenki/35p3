from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import numpy as np
import sys
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import grovepi

BP = brickpi3.BrickPi3() 
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS)
RIGHT = BP.PORT_A
LEFT = BP.PORT_D

def one_block (direction, x_or_y, x, y):

# this code is not complete!! we need to test to see at
# what power and for what duration of time makes Oiler
# travel exactly one block, I also think it would be really
# helpful to have another file that we use to calibrate this power
# so we can keep time consistent, and calibrate on the day of testing
# so we don't have fluctations due to charge left in the battery
# and are just left guessing for what power to use
    BP.set_motor_power(LEFT, -speed)
    BP.set_motor_power(RIGHT, -speed)
    time.sleep(2)
    BP.set_motor_power(LEFT, 0)
    BP.set_motor_power(RIGHT, 0)
    print("shimmied one block")
    time.sleep(0.25)
    if x_or_y > 0:
        x += direction
        print(x)
        print(direction)
        print(y)
    else:
        y += direction
        print(y)
    return x, y
    
def turnRight(x_or_y, direction):
    first = BP.get_sensor(BP.PORT_3)
    break_turn = 0
    while break_turn != 1:
        sensorValues = BP.get_sensor(BP.PORT_3)
        if abs(first[0] - sensorValues[0]) < (90):
            BP.set_motor_power(RIGHT, 32)
            BP.set_motor_power(LEFT, -32)  
            print(first[0] - sensorValues[0])
        else:
            BP.set_motor_power(RIGHT, 0) 
            BP.set_motor_power(LEFT, 0) 
            break_turn = 1
        time.sleep(0.025)

    x_or_y *= -1
    direction *= x_or_y
    return x_or_y, direction

def turnLeft(x_or_y, direction):
    first = BP.get_sensor(BP.PORT_3)
    break_turn = 0
    while break_turn != 1:
        sensorValues = BP.get_sensor(BP.PORT_3)
        if abs(first[0] - sensorValues[0]) < (90):
            BP.set_motor_power(RIGHT, -32)
            BP.set_motor_power(LEFT, 32)  
            print(first[0] - sensorValues[0])
        else:
            BP.set_motor_power(RIGHT, 0) 
            BP.set_motor_power(LEFT, 0) 
            break_turn = 1
        time.sleep(0.025)
 
    direction *= x_or_y
    x_or_y *= -1
    return x_or_y, direction

def orient(x_or_y, direction, please):
    if please != x_or_y:
        if direction_wanted == (direction * x_or_y):
            turnLeft(x_or_y,direction)
        else:
            turnRight(x_or_y,direction)
    elif (please == x_or_y) and (direction_wanted != direction) :
        turnRight(180)
    else:
        print('already right direction bozo')
    return x_or_y
    
x_please = 1
y_please = -1 

speed = int(input("desired speed for testing: "))

# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")

# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND
urFront = 2
urRight = 7
urLeft = 4


turn_speed = speed * 1.5
stop = 0


direction = 1 # 1 is right/up -1 is left/down
x_or_y = 1    # 1 is x_coord, -1 is y_coord
x = 0 
y = 0

course = ([1, 0, 0, 0], 
          [0, 0, 0, 0], 
          [0, 0, 0, 0], 
          [0, 0, 0, 0])

obstacle1_x = 3
obstacle1_y = 3
obstacle2_x = 3
obstacle2_y = 3
course[obstacle1_x][obstacle1_y] = -9999
course[obstacle2_x][obstacle2_y] = -9999

test = int(input("task 3 or 4? "))
target_x = []
target_y = []

if test == 4:
    p1_x = 2
    p1_y = 2
    p2_x = 1
    p2_y = 3
    p3_x = 0
    p3_y = 0
    p4_x = 3
    p4_y = 3
    
    target_x.append(p1_x)
    target_y.append(p1_y)
    course[target_x[0]][target_y[0]] = 25
    
    target_x.append(p2_x)
    target_y.append(p2_y)
    course[target_x[1]][target_y[1]] = 25
    
    target_x.append(p3_x)
    target_y.append(p3_y)
    course[target_x[2]][target_y[2]] = 25
    
    target_x.append(p4_x)
    target_y.append(p4_y)
    course[target_x[3]][target_y[3]] = 25
    point_count = 4
    
elif test == 3:
    p1_x = 1
    p1_y = 2
    target_x.append(p1_x)
    target_y.append(p1_y)
    course[target_x[0]][target_y[0]] = 25
    point_count = 1
    
point_num = 0
try:
    while point_num < point_count:
        
        if x != target_x[point_num]: # get x coord before y
            direction_wanted = int((target_x[point_num] - x) / (abs(target_x[point_num] - x))) # to get a 1 or -1
            if course[x + direction_wanted][y] > -1: # making sure the next block is safe
                orient(x_or_y, direction, x_please)
                one_block(direction, x_or_y, x, y)
            else:
                if y != target_x[point_num]:
                    direction_wanted = (target_y[point_num] - y) / (abs(target_y[point_num] - y))
                    if course[x][y + direction_wanted] > -1: # making sure the next block is safe
                        orient(x_or_y, direction, y_please)
                        one_block(direction, x_or_y, x, y)
                    # code here to get out of a stuck area I don't want to think about logically yet
                    # also, we always need to make sure that we don't go to a y or x value not on the course
        elif y != target_x[point_num]:
            print('already in correct x coord')
            direction_wanted = (target_y[point_num] - y) / (abs(target_y[point_num] - y))
            if course[x][y + direction_wanted] > -1: # making sure the next block is safe
                orient(x_or_y, direction, y_please)
                one_block(direction, x_or_y, x, y)
            else:
                if x != target_x[point_num]: # get x coord before y
                    direction_wanted = (target_x[point_num] - x) / (abs(target_x[point_num] - x)) # to get a 1 or -1
                    if course[x + direction_wanted][y] > -1: # making sure the next block is safe
                        orient(x_or_y, direction, x_please)
                        one_block(direction, x_or_y, x, y)

        if (x == target_x[point_num]) and (y == target_y[point_num]):
            point_num += 1
            
except KeyboardInterrupt:
    print("ctrl + c")
    BP.reset_all()
    sys.exit

