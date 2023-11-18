# -*- coding: utf-8 -*-
"""
Created on Thu May 27 23:14:03 2021

@author: printer
"""

# Import modules
import os
import sys
import serial 
import time
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI

# cd C:\Users\Biointerface\Documents\uArmPython\examples\Template

# Import my modules
import transform 
import gcodemod

# Import Arduino
ArduinoSerial = serial.Serial('COM4',2400) #COM5 is the port of syringe pump
time.sleep(2)

# Import uArm
swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
swift.waiting_ready(timeout=3)
device_info = swift.get_device_info()
print(device_info)
firmware_version = device_info['firmware_version']
if firmware_version and not firmware_version.startswith(('0.', '1.', '2.', '3.')):
    swift.set_speed_factor(0.0005)
swift.set_mode(0)

# Function
def my_range(start, end, step):
    while start >= end:
        yield start
        start = start-step

# Load Gcode
spp = 35  # Printing speed
spnp = 1000  # Not printing speed 
Z0 = 83 # starting z position
printhead=int(input(printhead number?2/3))
if printhead==3:
    a=280.7
    b=-2
if printhead==2:
    a=280.6
    b=70.5
x_cor=[7,7,7,0,0,0,-7,-7,-7]
y_cor=[7,0,-7,-7,0,7,7,0,-7]
xyarm_cir = transform.coordinateTransfer(x_cor, y_cor, a, b,33).T     
#offset = [0, 0, Z0] # Setting as [0,0,Z0] means printing at the central point (a_gcode,b_gcde) of the stage at Z0
da=-2#horizental deviation(---)
db=0#vertical deviation(l)


# set arduino

# Print to std out for checking gcode!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()
k=int(input('type the starting sequence [1,9]'))-1
# Start here-------
print('\nMove to the first circle position')
swift.flush_cmd(wait_stop=True)
swift.set_position(x=xyarm_cir[k][0]+da, y=xyarm_cir[k][1]+db, z=10, speed=3000, timeout=20)
time.sleep(1)
swift.set_position(x=xyarm_cir[k][0]+da, y=xyarm_cir[k][1]+db, z=Z0, wait=True)


# Print to std out for checking Z0!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    a = swift.get_position(wait=True, timeout=None, callback=None)
    swift.set_position(x=a[0], y=a[1], z=10, wait=True)
    swift.set_position(x=150, y=0, z=10, wait=True)
    swift.set_position(x=105, wait=True)
    swift.set_position(z=20, wait=True)
    swift.set_position(x=115, wait=True)
    swift.set_position(x=105, wait=True)
    sys.exit()
    
print('\nStart gcode printing')
swift.set_buzzer(frequency=3000, duration=0.1)

ArduinoSerial.write(b'6') # Turn on printhead 6, sucking
    #if input('type y if ok: ')=='y':
isTerminate = input('sucking complete? Please type any key to continue Y/n: ')
if isTerminate == 'n':
    ArduinoSerial.write(b'5')
    a = swift.get_position(wait=True, timeout=None, callback=None)
    swift.set_position(x=a[0], y=a[1], z=10, wait=True)
    swift.set_position(x=150, y=0, z=10, wait=True)
    swift.set_position(x=105, wait=True)
    swift.set_position(z=20, wait=True)
    swift.set_position(x=115, wait=True)
    swift.set_position(x=105, wait=True)
    sys.exit()
ArduinoSerial.write(b'5')
swift.set_position(z=10, speed=3000, wait=True)
swift.set_position(x=xyarm_cir[7][0]+da, y=xyarm_cir[7][1]+db, z=Z0-2, wait=True)
    #if input('type y if plate is ready: ')=='y':
isTerminate = input('plate ready? Please type any key to continue Y/n: ')
if isTerminate == 'n':
    a = swift.get_position(wait=True, timeout=None, callback=None)
    swift.set_position(x=a[0], y=a[1], z=10, wait=True)
    swift.set_position(x=150, y=0, z=10, wait=True)
    swift.set_position(x=105, wait=True)
    swift.set_position(z=20, wait=True)
    swift.set_position(x=115, wait=True)
    swift.set_position(x=105, wait=True)
    sys.exit()
ArduinoSerial.write(b'3')
isTerminate = input('finished? Please type any key to continue Y/n: ')
if isTerminate == 'n':
    ArduinoSerial.write(b'5')
    a = swift.get_position(wait=True, timeout=None, callback=None)
    swift.set_position(x=a[0], y=a[1], z=10, wait=True)
    swift.set_position(x=150, y=0, z=10, wait=True)
    swift.set_position(x=105, wait=True)
    swift.set_position(z=20, wait=True)
    swift.set_position(x=115, wait=True)
    swift.set_position(x=105, wait=True)
    sys.exit()
    
ArduinoSerial.write(b'5') # Turn off all printheads at the end
swift.set_buzzer(frequency=3000, duration=0.1)
print('\nGcode printing finished')  

print('\nLowering nozzle to z = 10')
swift.set_position(z=10, speed=3000, wait=True)
print('......')

# Always return to the initial position!!! 
print('\nReturn to starting position.(around X95 Y0 Z20)')
swift.set_position(x=200, y=0, z=10, wait=True)
swift.flush_cmd()
swift.set_position(x=150, y=0, z=10, wait=True)
swift.flush_cmd()
swift.set_position(x=130, y=0, z=10, wait=True)
swift.set_position(z=20, wait=True)
swift.set_position(x=115, wait=True)
swift.set_position(x=105, wait=True)
swift.flush_cmd()
swift.flush_cmd()
swift.set_buzzer(frequency=1000, duration=0.1)
time.sleep(2)
ArduinoSerial.close()