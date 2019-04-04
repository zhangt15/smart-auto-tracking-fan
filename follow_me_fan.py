###########################################
#       FOLLOW ME FAN - CAPSTONE CODE
#    Group: Tian, Justin, Will, Pavneet
###########################################

"""
Steps to Run:
1. Command Terminal -> sudo pcmanfm
2. Navigate to code and open
3. Make sure pigpio daemon is running
        - To do so: Command Terminal -> 'sudo pigpiod'
4. Run - Run Module (F5)
5. Kill pigpio daemon
        - To do so: Command Terminal -> 'sudo killall pigpiod'
6. Close *.py file

IMPORTANT NOTES:
- Columns correspond to x-direction
- Rows correspond to y-direction

In testing, the top of the matrix corresponds to a lower vertical height
and the bottom of the matrix corresponds to a greater vertical height


TO DO:
- Face detection code, so it doesn't move if you haven't moved***
- Clean up and comment code
"""

#################################
#         LIBRARIES
#################################

import sys
import subprocess
import pigpio
#import os
sys.path.insert(0,"/home/pi/.local/lib/python3.5/site-packages")
#from tkinter import *
import time
#from time import sleep
import wavePWM
import busio
import board
import numpy as np
import math
#import colorsys
#from PIL import Image
import MLX90640 as x


#################################
#         FUNCTIONS
#################################

def motorX_movement(pulse_width_X):
        """
        Controls X-direction servo motor via pulse width
        Pulse width calculated from duty cycle in While Loop
        """
        pi.set_servo_pulsewidth(18,pulse_width_X)
        #pi.set_PWM_dutycycle(18, duty)

def motorX_movement_mid():
        """
        Sets servo motor in the X-direction to Midpoint
        """
        pi.set_servo_pulsewidth(18,1500)
        #pi.set_PWM_dutycycle(18, duty)

def motorY_movement(pulse_width_Y):
        """
        Controls Y-direction servo motor via pulse width
        Pulse width calculated from duty cycle in While Loop
        """
        pi.set_servo_pulsewidth(23,pulse_width_Y) #SERVO[1] -> 23

def motorY_movement_mid():
        """
        Sets servo motor in the Y-direction to Midpoint
        """
        pi.set_servo_pulsewidth(23,1600) #SERVO[1] -> 23 
        
def split_1d(arr_2d):
        """
        Returns 2 1-D arrays when given a single 2-D array
        Used for Bincount/Binning
        """
        split = np.hsplit(arr_2d,arr_2d.shape[1])
        split = [np.squeeze(arr) for arr in split]
        return split


#################################
#        Initialization
#################################

#Initialization of constants
SERVO = [18,23]
#^^^ replace all 18's with SERVO[0] and all 23's with SERVO[1]
prev_personArray = [16,12]
prevprev_personArray = [16,12]

#Initialization of global arrays:
masterArray = []
OneArray = []
store_binArray_leftRow = []
store_binArray_leftCol = []


#Initialization of pigpio variables:

pi = pigpio.pi()

if not pi.connected:
        exit()

#IS THIS NEEDED????
pwm = wavePWM.PWM(pi)
cl = pwm.get_cycle_length()
pwm.set_pulse_start_and_length_in_micros(18, cl/10, cl/2)
#print ("Cycle Length: " + str(cl))
#print ("GPIO Settings: " + str(pwm.get_GPIO_settings(18)))

#pi.set_PWM_range(18, 100)
#pi.set_PWM_range(23, 100)
pi.set_mode (18, pigpio.OUTPUT) #GPIO 18 as output
pi.set_mode (23, pigpio.OUTPUT) #GPIO 23 as output

#pi.set_PWM_range(18, 100)
#pi.set_PWM_range(23, 100)
#pi.set_PWM_frequency(18, 100000)
#pi.set_PWM_frequency(23, 5000)

#Initialization of Misc. global variables:

hor_angle = 1
prev_hor_angle = 360
"""
^^^ Absurd value used to ensure that new angle is used on the
first deadband comparison
"""

db_hor_angle = 10 # Originally 10, set it equal to 2 in testing
"""
^^^ If the difference in angle between 2 frames is less than 10 degrees
the servo-motor will not move
"""
vert_angle = 1
prev_vert_angle = 60
db_vert_angle = 5

#CUTOFF_TEMP = 29
cutoff_temp = 29
"""
Notes: pwm.start(duty cycle) where duty cycle corresponds to
percentage as opposed to decimal -IS THIS NOTE NEEDED ANY LONGER?????
"""

#Horizontal Angle Initalization:

#horizontal_angle = np.arange(10,170,5)
tran_horizontal_angle = np.arange(170,10,-5) #32 entries, for the columns
#tran_horizontal_angle = np.arange(10,170,5) #TEST
horizontal_angle = tran_horizontal_angle
#print (horizontal_angle)
#print (tran_horizontal_angle)

#Vertical Angle Initalization

#vertical_angle = [8]
vertical_angle = np.arange(75,106.25,1.25) #24 entries, for the rows

motorX_movement_mid()
motorY_movement_mid()


#################################
#            MAIN
#################################

print ("CAMERA/SERVO TEST - START")

try:
        while True:

                print("in")
                #Thermal Video - Interp File (uncomment to display)
                #proc = subprocess.run(["/home/pi/.local/lib/python3.5/site-packages/mlx90640-library/interp"])

                x.setup(16)
                f = x.get_frame()
                x.cleanup()

                #motorX_movement_mid(1500)

                temp_min = min(f)
                temp_max = max(f)

                #Ambient Cutoff Temperature
                scaling_fact = 0.96 #SET AS POTENTIAL GLOBAL VAR?
                temp_scaling = (temp_max - temp_min)*scaling_fact + temp_min
                cutoff_temp = scaling_fact*temp_max

                print('\n')
                print('Min Temp: %f' % (temp_min))
                print('Max Temp: %f' % (temp_max))

                np.array(f)

                #All our temperature values
                masterArray = np.reshape(f,(24,32))

                #Temps converted to 1s and 0s based on cutoff_temp
                masterArray = (masterArray > cutoff_temp).astype(int)

                """
                Creating a 2-D array of nonzero counts and tranposing
                nx2 array
                """
                OneArray = np.transpose(np.nonzero(masterArray))

                """
                splitting OneArray into 2 nx1 arrays.
                one for rows, one for columns
                """
                oneArray_leftRow, oneArray_leftCol = split_1d(OneArray)

                """
                Binning everything,
                dynamic array of size nxm where n is up to 24 and m is up to 32
                """
                try:
                        binArray_leftRow = np.bincount(oneArray_leftRow)
                        binArray_leftCol = np.bincount(oneArray_leftCol)

                        #Store last frames values for exception handling
                        store_binArray_leftRow = binArray_leftRow
                        store_binArray_leftCol = binArray_leftCol
                        
                except ValueError:
                        binArray_leftRow = store_binArray_leftRow
                        binArray_leftCol = store_binArray_leftCol
                        pass

                #find the max in the bins
                conLeftOne_Row = max(binArray_leftRow)
                conLeftOne_Col = max(binArray_leftRow)

                #indices correpsond to top of block of 1s
                leftTop_ptRow = np.argmax(binArray_leftRow)
                leftTop_ptCol = np.argmax(binArray_leftCol)

                #Rounding Stuff: Check if consecutive row of one numbers is odd or even
                if (conLeftOne_Row % 2) == 0:
                        #math.ceil -> forces number to be rounded up
                        rightBot_ptRow = (leftTop_ptRow + math.ceil(conLeftOne_Row/2))
                        rightBot_ptCol = (leftTop_ptCol + math.ceil(conLeftOne_Col/2))
                        
                else:
                        rightBot_ptRow = (leftTop_ptRow + math.ceil(conLeftOne_Row/2)) - 1
                        rightBot_ptCol = (leftTop_ptCol + math.ceil(conLeftOne_Col/2)) - 1

                #To catch outside boundary cases
                if rightBot_ptRow > 23:
                        rightBot_ptRow = 23
                if rightBot_ptCol > 31:
                        rightBot_ptCol = 31
                        
                print (masterArray)

                hor_ind_even = (leftTop_ptRow + rightBot_ptRow)%2
                vert_ind_even = (leftTop_ptCol + rightBot_ptCol)%2

                #columns correspond to x-direction
                #rows correspond to y-direction
                y_coord = int ((leftTop_ptRow + rightBot_ptRow)/2) #Switched 
                x_coord = int ((leftTop_ptCol + rightBot_ptCol)/2)
                
                #Print Leftmost Point Coordinates
                print ('Left Col Value: %s at Index %s' % (conLeftOne_Col,leftTop_ptCol)) #Switched
                print ('Left Row Value: %s at Index %s' % (conLeftOne_Row,leftTop_ptRow))
                print ('Leftmost Point: (%s,%s)' % (leftTop_ptCol,leftTop_ptRow))

                #Print Rightmost Point Coordinates
                print ('Rightmost Point: (%s,%s)' % (rightBot_ptCol,rightBot_ptRow)) #Switched

                #Print Person's coordinates
                print ("Person's coordinates: (%s,%s)" % (x_coord, y_coord))
                personArray = [x_coord,y_coord]


                #Global Areray --> prev_personArray AND prevprev_personArray
                
                first_Compare = np.allclose(prev_personArray,personArray,0.06,2.5)
                second_Compare = np.allclose(prevprev_personArray,personArray,0.06,2.5)#0.05,2
                print ('First Compare: ' + str(first_Compare))
                print (prev_personArray)
                print ('Second Compare: ' + str(second_Compare))
                print (prevprev_personArray)

                prevprev_personArray = prev_personArray

                if first_Compare == False and second_Compare == False:

                        print('update values')
                        prev_personArray = personArray
                
                        #Horizontal angle
                        if hor_ind_even==0:
                                hor_angle = horizontal_angle[x_coord] #angle = horizontal_angle[prev_max_temp_row - 1] 
                        else:
                                if x_coord == 31:
                                        hor_angle = horizontal_angle[x_coord] 
                                else:
                                        hor_angle = (horizontal_angle[x_coord] + horizontal_angle[x_coord+1])/2

                        #If hor_angle is within deadband, do not move fan
                        if (abs(hor_angle - prev_hor_angle) < db_hor_angle):
                                hor_angle = prev_hor_angle

                        #Vertical angle
                        if vert_ind_even==0:
                                vert_angle = vertical_angle[y_coord] 
                        else:
                                if y_coord == 23:
                                        vert_angle = vertical_angle[y_coord]
                                else:
                                        vert_angle = (vertical_angle[y_coord] + vertical_angle[y_coord+1])/2
                        #If vert_angle is within deadband, do not move fan
                        if (abs(vert_angle - prev_vert_angle) < db_vert_angle):
                                vert_angle = prev_vert_angle

                        """
                        Note: consider using a flag to tell the PWM when
                        we want to update the dc
                        """
                        #print(angle)
                        #print(float(angle))

                        #TO DO: WORK ON DUTY->PULSE WIDTH CODE ****
                        
                        duty = float(hor_angle) / 10.0 + 2.5
                        print("X-Duty: "  + str(duty))
                        #pulse_width = (duty/100) * cl + 1000
                        pulse_width_X = 50 * duty + 1000

                        duty2 = float(vert_angle) / 10.0 + 2.5
                        pulse_width_Y = 50 * duty2 + 1000
                        #print("Y-Duty: "  + str(duty2))

                        #Code to prevent damage to Servo Motor
                        if pulse_width_X > 2000:
                                pulse_width_X = 2000
                                print("*** PULSE WIDTH X IS ABOVE SAFE PARAMETERS ***")
                        if pulse_width_X < 1000:
                                pulse_width_X = 1000
                                print("*** PULSE WIDTH X IS BELOW SAFE PARAMETERS ***")
                        if pulse_width_Y > 2000:
                                pulse_width_Y = 2000
                                print("*** PULSE WIDTH Y IS ABOVE SAFE PARAMETERS ***")
                        if pulse_width_Y < 1000:
                                pulse_width_Y = 1000
                                print("*** PULSE WIDTH Y IS BELOW SAFE PARAMETERS ***")

                        
                        print("Servo Pulse Width X: "  + str(pulse_width_X))
                        #print("Servo Pulse Width Y: "  + str(pulse_width_Y))
                        
                        #Motor Movment
                        motorX_movement(pulse_width_X)
                        motorY_movement(pulse_width_Y)

                        #time.sleep(1)
                        
                else:
                        print('they are close enough')
                        prev_personArray = personArray

except KeyboardInterrupt:
        print("CTRL-C: Program Stopping via Keyboard Interrupt...")

        #Uncomment when display camera code is uncommented
        #proc.terminate()

#Handles unexpected errors
except:
        print("Unexpected error: ", sys.exc_info()[0])
        raise

finally:
        motorX_movement_mid()
        motorY_movement_mid()
        print("Exiting Loop...")
        print ("CAMERA/SERVO TEST - FINISHED")

