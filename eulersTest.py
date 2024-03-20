from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''
from MPU9250 import MPU9250

import numpy as np
import sys
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
mpu9250 = MPU9250()

try:
    gyro = mpu9250.readGyro()
    
    RIGHT = BP.PORT_A
    LEFT = BP.PORT_D
    BP.offset_motor_encoder(RIGHT, BP.get_motor_encoder(RIGHT))
    BP.offset_motor_encoder(LEFT, BP.get_motor_encoder(LEFT))

    desiredAngle = int(input("desired angle: "))
    theta = 0
    h = 0.001
    x = 0
    while x != 1:
       
        gyro_x = gyro['x']
        gyro_y = gyro['y']
        gyro_z = gyro['z']

        if theta < desiredAngle * 2:
            BP.set_motor_power(RIGHT, 32)
            BP.set_motor_power(LEFT, -32)  
            degree = np.sqrt((gyro_z**2 + gyro_y**2)) * 180 / np.pi  
            theta = theta + h*degree   
            print(f"z: {gyro_z}; y: {gyro_y} degree: {degree}")
            print(f"angle: {theta}")
            x = 1
        else:
            BP.set_motor_power(RIGHT, 0) 
            BP.set_motor_power(LEFT, 0) 
        print(gyro)
        time.sleep(0.025)

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
