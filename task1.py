from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''


import numpy as np
import sys
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
BP.set_sensor_type(BP.PORT_3, BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS)


try:
    time.sleep(4)
    first = BP.get_sensor(BP.PORT_3)
    print(first)
    RIGHT = BP.PORT_A
    LEFT = BP.PORT_D
    BP.offset_motor_encoder(RIGHT, BP.get_motor_encoder(RIGHT))
    BP.offset_motor_encoder(LEFT, BP.get_motor_encoder(LEFT))

    desiredAngle = int(input("desired angle: "))

    theta = 0
    x = 0

    while x != 1:
        sensorValues = BP.get_sensor(BP.PORT_3)
        if abs(first[0] - sensorValues[0]) < (desiredAngle - 7):
            print(abs(first[0] - sensorValues[0]))
            BP.set_motor_power(RIGHT, 32)
            BP.set_motor_power(LEFT, -32)  
            #print(sensorValues[0])
        else:
            BP.set_motor_power(RIGHT, 0) 
            BP.set_motor_power(LEFT, 0) 
            x = 1
        time.sleep(0.025)

except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
    BP.reset_all()        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
    sys.exit()
