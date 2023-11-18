# -*- coding: utf-8 -*-
"""
Created on Fri Jul 15 01:12:23 2022

@author: printer
"""

import os
import sys
import serial 
import time
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI
import keyboard

# cd C:\Users\Biointerface\Documents\uArmPython\examples\Template

# Import my modules
import transform 
import gcodemod

# Import Arduino
ArduinoSerial = serial.Serial('COM4',2400) #COM3 is the port of syringe pump
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
spp = 400  # Printing speed
spnp = 1000  # Not printing speed 
Z0 = 82 # starting z position
#offset = [-5, -5, Z0] # Setting as [0,0,Z0] means printing at the central point (a_gcode,b_gcde) of the stage at Z0
printhead = 5 #printhead for portabel one
stage = 3 #1 Small, 2 Large, 384 well plate

num=0
x_o=0
y_o=0

# X-Y coordinates transformation
ab = [[282.5,76], [282.5,1.5], [280,-74], [267,-5]] #Calibrated printhead 2,3,4 a,b coordinates
stage_mega_r = [33, 44.5, 78]
a_gcode = ab[printhead-2][0] # x coord of the printhead from uArm base, mm 
b_gcode = ab[printhead-2][1] # y coord of the printhead from uArm base, mm
r_stage = stage_mega_r[stage-1]
swift.set_position(a_gcode-r_stage, b_gcode, 10, speed=3000, timeout=20)
swift.set_position(a_gcode-r_stage, b_gcode, Z0, speed=3000, timeout=20)

iscalibration = input('Need calibration? Please type y to calibration, or any other key to skip: ')
if iscalibration == 'y':
         
    while True:
        z_s=float(input('z_shift'))
        Z0+=z_s
        swift.set_position(a_gcode-r_stage, b_gcode, Z0, speed=3000, timeout=20)
        isTerminate = input('Continue? Please type y to process forward: ')
        if isTerminate == 'y':
             break
    
    while True:
        y_s=float(input('x_shift'))
        a_gcode+=y_s
        swift.set_position(a_gcode-r_stage, b_gcode, Z0, speed=3000, timeout=20)
        isTerminate = input('Continue? Please type y to process forward: ')
        if isTerminate == 'y':
            break 
        
    while True:
        x_s=float(input('y_shift'))
        b_gcode+=x_s
        swift.set_position(a_gcode-r_stage, b_gcode, Z0, speed=3000, timeout=20)
        isTerminate = input('Continue? Please type y to process forward: ')
        if isTerminate == 'y':
            break
x_f=[0]
y_f=[0]
xa=x_f[0]
ya=y_f[0]
xy_gcode = transform.coordinateTransfer(x_f, y_f, a_gcode, b_gcode, r_stage).T
# move to the center of the first well.
swift.set_position(xy_gcode[0,0], xy_gcode[0,1], 10, speed=3000, timeout=20)
swift.set_position(xy_gcode[0,0], xy_gcode[0,1], Z0, speed=3000, timeout=20)

i=1
a=[]
while i<=24:
    print('adjust the printhead position to the start row')    
    while True:
        y_s=float(input('y_shift'))
        y_f[0]+=y_s
        xy_gcode = transform.coordinateTransfer(x_f, y_f, a_gcode, b_gcode, r_stage).T
        swift.set_position(xy_gcode[0,0], xy_gcode[0,1], Z0, speed=3000, timeout=20)
        isTerminate = input('Continue? Please type y to process forward: ')
        if isTerminate == 'y':
            break 

    while True:
        x_s=float(input('x_shift'))
        x_f[0]+=x_s
        xy_gcode = transform.coordinateTransfer(x_f, y_f, a_gcode, b_gcode, r_stage).T
        swift.set_position(xy_gcode[0,0], xy_gcode[0,1], Z0, speed=3000, timeout=20)
        isTerminate = input('Continue? Please type y to process forward: ')
        if isTerminate == 'y':
            break 
    offset=[x_f[0], y_f[0], Z0]
    a.append(offset)
    i+=1
    
print(a)
