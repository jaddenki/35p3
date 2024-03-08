from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import numpy as np
import sys
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import grovepi



# set I2C to use the hardware bus
grovepi.set_bus("RPI_1")

# Connect the Grove Ultrasonic Ranger to digital port D4
# SIG,NC,VCC,GND
urFront = 2

BP = brickpi3.BrickPi3() 
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS)
RIGHT = BP.PORT_A
LEFT = BP.PORT_D
speed = int(input("desired speed for testing: "))
x = 0
y = 0
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
            
            # turn right !!!
            first = BP.get_sensor(BP.PORT_3)
            print(first)
            x = 0
            while y != 1:
                sensorValues = BP.get_sensor(BP.PORT_3)
                if abs(first[0] - sensorValues[0]) < (90):
                    BP.set_motor_power(RIGHT, 32)
                    BP.set_motor_power(LEFT, -32)  
                    print(first[0] - sensorValues[0])
                else:
                    BP.set_motor_power(RIGHT, 0) 
                    BP.set_motor_power(LEFT, 0) 
                    y = 1
                time.sleep(0.025)

            time.sleep(1)
            BP.set_motor_power(LEFT, -speed)
            BP.set_motor_power(RIGHT, -speed)
            time.sleep(2)
            BP.set_motor_power(LEFT, 0)
            BP.set_motor_power(RIGHT, 0)
            print("I turned right.")    
            y = 0 
            x = 1  
            
except KeyboardInterrupt:
    print("ctrl + c")
    BP.reset_all()
    sys.exit
