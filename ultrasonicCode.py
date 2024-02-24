from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''
from MPU9250 import MPU9250
import numpy as np
import sys
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import grovepi
mpu9250 = MPU9250()


# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")

# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND
urFront = 2
gyro = mpu9250.readGyro()


def turnRight():
    desiredAngle = 90
    theta = 0
    h = 0.001
    y = 0
    while y != 1:
        gyro_x = gyro['x']
        gyro_y = gyro['y']
        gyro_z = gyro['z']
        if theta < desiredAngle * 2:
            BP.set_motor_power(RIGHT, 32)
            BP.set_motor_power(LEFT, -32)  
            degree = np.sqrt((gyro_z**2 + gyro_y**2)) * 180 / np.pi  
            theta = theta + h*degree   
        else:
            BP.set_motor_power(RIGHT, 0) 
            BP.set_motor_power(LEFT, 0) 
            y = 1
        print(gyro)
        time.sleep(0.025)


BP = brickpi3.BrickPi3() 
RIGHT = BP.PORT_A
LEFT = BP.PORT_D
speed = int(input("desired speed for testing: "))
x = 0

try:
    while x != 1:
        reading = grovepi.ultrasonicRead(urFront)
        if reading > 7:
            BP.set_motor_power(LEFT, -speed)
            BP.set_motor_power(RIGHT, -speed)
        else:
            BP.set_motor_power(LEFT, 0)
            BP.set_motor_power(RIGHT, 0)
            time.sleep(1)
            
            turnRight()
            
            time.sleep(1)
            BP.set_motor_power(LEFT, -speed)
            BP.set_motor_power(RIGHT, -speed)
            time.sleep(2)
            BP.set_motor_power(LEFT, 0)
            BP.set_motor_power(RIGHT, 0)
            print("I turned right.")     
            x = 1  
            
except KeyboardInterrupt:
    print("ctrl + c")
    BP.reset_all()
    sys.exit
