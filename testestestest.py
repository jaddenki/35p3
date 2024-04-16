from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       

import numpy as np
import sys
import time     # import the time library for the sleep function

# Functions =======================================================

def turnRight():
    print("I turn right")
    time.sleep(0.2)
            
def turnLeft():
    print("I turn left")
    time.sleep(0.2)

def goForward():
    print("I went forward once!")
   # print(place)
            
# Variables ==================================================

cpx = int(input("current point x: "))
cpy = int(input("current point y: "))
print("~~~~~~~~~~~~~~~~")
wpx = int(input("wanted point x: "))
wpy = int(input("wanted point y: "))
x = 1
pos = input("current orientation (left, right, up, down): ")

# List stuff idk ============================================

# number of arrays = y position + 1 (indexing is just y)
# items in arrays = x position
place = [[0]] # 0 is dark


# Logic =====================================================

print(place)
try:
    while (x == 1):
        print(f'({cpx}, {cpy})')
        print(f'position: {pos}')
        if ((cpx == wpx) and (cpy == wpy)):
            x = 0
        else:
            while (cpx != wpx): 
                if (cpx < wpx):
                    if (pos == 'up'):
                        turnRight()
                        pos = 'right'
                    elif (pos == 'left'):
                        turnLeft()
                        turnLeft()
                        pos = 'right'
                    elif (pos == 'down'):
                        turnLeft()
                        pos = 'right'
                    goForward()
                    cpx += 1
                    place[cpy].append(0)
                    
                elif (cpx > wpx):
                    if (pos == 'right'):
                        turnLeft()
                        turnLeft()
                        pos = 'left'
                    elif (pos == 'up'):
                        turnLeft()
                        pos = 'left'
                    elif (pos == 'down'):
                        turnRight()
                        pos = 'left'
                    goForward()
                    cpx -= 1
            while (cpy != wpy):
                if (cpy < wpy):
                    if (pos == 'right'):
                        turnLeft()
                        pos = 'up'
                    elif (pos == 'left'):
                        turnRight()
                        pos = 'up'
                    elif (pos == 'down'):
                        turnLeft()
                        turnLeft()
                        pos = 'up'
                    goForward()
                    cpy += 1
                    place.append([])
                    for i in range(0, cpx, 1):
                        place[cpy].append(1)
                    place[cpy].append(0)
                        
                elif (cpy > wpy):
                    if (pos == 'right'):
                        turnRight()
                        pos = 'down'
                    elif (pos == 'up'):
                        turnLeft()
                        turnLeft()
                        pos = 'down'
                    elif (pos == 'left'):
                        turnLeft()
                        pos = 'down'
                    goForward()
                    cpy -= 1
            
    print(place)                    
except KeyboardInterrupt:
    print("u pressed ctrl + c")
    sys.exit