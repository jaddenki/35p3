from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import sys

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
RIGHT = BP.PORT_A
LEFT = BP.PORT_D


try:
    while True:
        #speed for both
        speed = int(input("desired speed for testing: "))
        BP.set_motor_power(LEFT, -speed)
        BP.set_motor_power(RIGHT, -speed)
        
except KeyboardInterrupt:
    BP.reset_all()
    sys.exit




