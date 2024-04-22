import time
import statistics as s
from MPU9250 import MPU9250
import grovepi
import brickpi3 # import the BrickPi3 drivers



# IDK =========================================================================

grovepi.set_bus("RPI_1")

# ultrasonic
front = 8
left = 3 

# ir
one = 14		# Pin 14 is A0 Port.
two = 15		# Pin 15 is A0 Port.     
grovepi.pinMode(one,"INPUT")
grovepi.pinMode(two,"INPUT")     

# magnet
mpu9250 = MPU9250()  
BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.EV3_GYRO_ABS_DPS)

RIGHT = BP.PORT_A
LEFT = BP.PORT_D
BACK = BP.PORT_B    

# Functions =======================================================

def turnRight(turnAmt):
    print("I turn right")
    y = 0 # has not turned yet
    first = BP.get_sensor(BP.PORT_1) # initial position
    while y != 1:
        sensorValues = BP.get_sensor(BP.PORT_1)
        if (sensorValues[0]) < (turnAmt+(first[0])):
            BP.set_motor_power(RIGHT, 20)
            BP.set_motor_power(LEFT, -20)  
        else:
            BP.set_motor_power(RIGHT, 0) 
            BP.set_motor_power(LEFT, 0) 
            y = 1
            time.sleep(0.025)
            
def turnLeft(turnAmt):
    print("I turn left")
    y = 0 # has not turned yet
    first = BP.get_sensor(BP.PORT_1) # initial position
    while y != 1:
        sensorValues = BP.get_sensor(BP.PORT_1)
        if (sensorValues[0]) > (first[0]-turnAmt):
            BP.set_motor_power(RIGHT, -20)
            BP.set_motor_power(LEFT, 20)  
        else:
            BP.set_motor_power(RIGHT, 0) 
            BP.set_motor_power(LEFT, 0) 
            y = 1
            time.sleep(0.025)

def goForward(amt):
    BP.set_motor_power(RIGHT, -30)
    BP.set_motor_power(LEFT, -30)
    time.sleep(amt)
    BP.set_motor_power(RIGHT, 0)
    BP.set_motor_power(LEFT, 0)
    print("I went forward once!")

def dropCargo(num):
    BP.set_motor_power(BACK, num)
    time.sleep(1)
    BP.set_motor_power(BACK, 0)
    time.sleep(1)
    print("I dropped a shit!")
    
# Calibration Process =========================================================

yes = input("\033[1;34;40mWant to start calibrating? \033[0;37;40m[y or n] \033[1;35;40m( ✿ ◠ ‿ ◠ ): \033[0;37;40m")
if (yes == "y"):
    choice = int(input("\033[1;35;40mWhat would you like to calibrate?\033[1;37;40m ≧ ◡ ≦ \n\033[0;37;40m1: Heat Source\n2: Magnetic Source\n3: Front Threshold\n4: Left Threshold\n5: Motors\n"))
    if choice == 1:
        try:
            print("Let's calibrate the \033[0;37;41mheat source!\033[1;37;40m o(╥﹏╥)o")
            dist = int(input("\033[0;33;40mHow far are you from the heat source? [cm]:\033[1;37;40m "))
            
            x = int(input("\033[0;32;40mType \"0\" when ready to calibrate:\033[0;37;40m "))
            heatval = []
            while (x < 15):
                irone  = grovepi.analogRead(one)
                irtwo = grovepi.analogRead(two)
                print(f"Current Value 1: {irone} | Current Value 2: {irtwo} | Current time: {(x + 1)/ 10} seconds")
                heatval.append((irone + irtwo) / 2)
                x += 1
                time.sleep(0.1)
            print("\n\033[1;36;40mResults!\033[0;37;40m")
            me = s.mean(heatval)
            st = s.stdev(heatval)
            print(f"Distance = {dist} cm or {float(dist) * 0.393701} in")
            print("Mean = " + str(me))
            print("STDEV = " + str(st))
            print(f"Recommended threshold is between {me - st} and {me + st}. thx! \n")
        except ValueError:
            print("\033[1;31;40mpoop u got an error. let's redo!\033[0;37;40m")
        
    elif choice == 2:
        try:
            print("Let's calibrate the \033[0;37;45mmagnetic source!\033[1;37;40m (｡-_-｡)")
            dist = int(input("\033[0;33;40mHow far are you from the magnetic source? [cm]:\033[1;37;40m "))
            
            x = int(input("\033[0;32;40mType \"0\" when ready to calibrate: \033[0;37;40m "))
            magval = []
            while (x < 15):
                mag  = mpu9250.readMagnet()['x']
                print(f"Current Value: {mag} | Current time: {(x + 1)/ 10} seconds")
                magval.append(mag)
                x += 1
                time.sleep(0.1)
            print("\n\033[1;36;40mResults!\033[0;37;40m")
            try:
                me = s.mean(mag)
                st = s.stdev(mag)
                print(f"Distance = {dist} cm or {float(dist) * 0.393701} in")
                print("Mean = " + str(me))
                print("STDEV = " + str(st))
                print(f"Recommended threshold is between {me - st} and {me + st}. thx! \n")
            except ArithmeticError:
                print("oopsie poopsie. do that shit urself")
        except ValueError:
            print("\033[1;31;40mpoop u got an error. let's redo!\033[0;37;40m")
                    
    elif choice == 4:
        try:
            print("Let's calibrate the \033[0;37;42mleft threshold!\033[1;37;40m ◕ 3 ◕")      
            x = int(input("\033[0;32;40mType \"0\" when ready to calibrate: \033[0;37;40m "))
            urlv = []
            while (x < 15):
                url  = grovepi.ultrasonicRead(left)
                print(f"Current Value: {url} | Current time: {(x + 1)/ 10} seconds")
                urlv.append(url)
                x += 1
                time.sleep(0.1)
            print("\n\033[1;36;40mResults!\033[0;37;40m")
            me = s.mean(urlv)
            st = s.stdev(urlv)
            print("Mean = " + str(me))
            print("STDEV = " + str(st))
            print(f"Recommended threshold is between {me - st} and {me + st}. thx! \n")
        except ValueError:
            print("\033[1;31;40mpoop u got an error. let's redo!\033[0;37;40m")
                            
    elif choice == 3:
        try:
            print("Let's calibrate the \033[0;37;44mfront threshold!\033[1;37;40m  ⊙ ﹏⊙")      
            x = int(input("\033[0;32;40mType \"0\" when ready to calibrate: \033[0;37;40m "))
            urlv = []
            while (x < 15):
                url  = grovepi.ultrasonicRead(front)
                print(f"Current Value: {url} | Current time: {(x + 1)/ 10} seconds")
                urlv.append(url)
                x += 1
                time.sleep(0.1)
            print("\n\033[1;36;40mResults!\033[0;37;40m")
            me = s.mean(urlv)
            st = s.stdev(urlv)
            print("Mean = " + str(me))
            print("STDEV = " + str(st))
            print(f"Recommended threshold is between {me - st} and {me + st}. thx! \n")
        except ValueError:
            print("\033[1;31;40mpoop u got an error. let's redo!\033[0;37;40m")            
    elif choice == 5:
        print("Commencing \033[0;37;44mmotor magic!!!!\033[1;37;40m  \nType [e] to exit. ⊙ ﹏⊙")
        option = 'hi'
        while (option != 'e'):
            try:
                option = input("Would you like to test turning [t] or cargo [c]?: ")
                if option == "t":
                    turnAmt = int(input("How much would you like to turn?: "))
                    direction = input("Would you like to turn right [r] or left [l]?: ")
                    if direction == 'r':
                        turnRight(turnAmt)
                    elif direction == 'l':
                        turnLeft(turnAmt)
                elif option == "c":
                    num = int(input("How much power would you like to use?: "))
                    dropCargo(num)
                elif option == "e":
                    break
            except brickpi3.SensorError as error:
                print(error)

else:
        print("why the fuck are you here \033[1;31;40mbitch\033[0;37;40m")
                                    