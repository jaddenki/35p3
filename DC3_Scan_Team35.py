from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''


import numpy as np
import sys
import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.NXT_LIGHT_ON)

RIGHT = BP.PORT_A
LEFT = BP.PORT_B

# Functions ===================================
def goForward():
    BP.set_motor_power(RIGHT, 10)
    BP.set_motor_power(LEFT, 10)
    time.sleep(0.15) # 1 cm
    BP.set_motor_power(RIGHT, 0)
    BP.set_motor_power(LEFT, 0)
    print("I went forward once!")
    time.sleep(0.2)
# Logic ======================================

x = 0

fid = open("DC3_Data.csv","w")

header = ['Values', 'x', 'y']

fid.write(str(header))
try:
    while x < 25:
        x = int(input("x value: "))
        y = 0
        fid.write("\n")

        while (y < 25):
            reading = BP.get_sensor(BP.PORT_1)
            fid.write(str(reading) + "," + str(x) + "," + str(y))
            fid.write("\n")
            goForward()
            y += 1
except KeyboardInterrupt:
    print("ctrl + c")
    sys.exit
    BP.reset_all()
    fid.close()
