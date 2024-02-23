
from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''
from MPU9250 import MPU9250

import sys
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
mpu9250 = MPU9250()

try:
    gain = 0.24 #  User can change this value to see how the behavior of the controller changes
    angle_delta = 360 # User can change this value to see how the behavior of the controller changes
    gyro = mpu9250.readGyro()
    
    RIGHT = BP.PORT_A
    LEFT = BP.PORT_D
    BP.offset_motor_encoder(RIGHT, BP.get_motor_encoder(RIGHT))
    BP.offset_motor_encoder(LEFT, BP.get_motor_encoder(LEFT))

    while True:

        current_offset = angle_delta - BP.get_motor_encoder(RIGHT)
        gyro_x = gyro['x']
        gyro_y = gyro['y']
        gyro_z = gyro['z']
        
        print("Start: " + gyro)
        
        if current_offset != 0:
            # Right
            BP.set_motor_power(RIGHT, current_offset*gain)
            # Left
            current_offset = angle_delta - BP.get_motor_encoder(LEFT)
            BP.set_motor_power(LEFT, -current_offset*gain)
        else:
            print(gyro)
            time.sleep(0.25)

    

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
