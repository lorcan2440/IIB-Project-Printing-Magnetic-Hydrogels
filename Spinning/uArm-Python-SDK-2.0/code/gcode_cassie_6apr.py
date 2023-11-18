# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 13:00:38 2022

@author: cassa
"""

# Import modules
import os
import sys
import serial 
import time
import numpy as np
import transform
import transform_reverse
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI
import keyboard 
import gcodemod

#import Arduino
ArduinoSerial = serial.Serial('COM5',2400) #COM4 is the port of syringe pump
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

def my_range(start, end, step):
    while start >= end:
        yield start
        start = start-step
        
#set the position of printhead origin wrt the arm base origin, for tamara's pdms mold (276.1, -4)     
# arm coord system denoted a , b
#our coord system denoted x , y
x0 = 250 # initial x
y0 = -4 # initial y 
z = 50 # initial z position
        
# Printing parameters
spp = 35 # printing speed
#n = 0
r_stage=44.5 #petridish radius
delaytime=10000 #corresponds to extrusion speed
length=len(str(delaytime))
offset = [0, 0, z] # Setting as [0,0,Z0] means printing at the central point (a_gcode,b_gcde) of the stage at Z0

bigCoor = gcodemod.read(r"C:\Users\49250\Documents\uArm-Python-SDK-2.0\code\sbox.txt", offset) # Import gcode

x_gcode = bigCoor[:, 0] # Import x coord from gcode file
y_gcode = bigCoor[:, 1] # Import y coord from gcode file
z_gcode = bigCoor[:, 2] # Import z coord from gcode file
e_gcode = bigCoor[:, 3]  # Import extrusion information from gcode file 

if length==1: #send first charater to the Arduino, let it know how many numbers it needs to wait before convert numbers in buffer into delaytime)
    ArduinoSerial.write(b'1')
if length==2:
    ArduinoSerial.write(b'2')
if length==3:
    ArduinoSerial.write(b'3')
if length==4:
    ArduinoSerial.write(b'4')
if length==5:
    ArduinoSerial.write(b'5')

for i in str(delaytime):#send numbers in the delaytime individually
    print(i)
    if int(i)==0:
        ArduinoSerial.write(b'0')
    if int(i)==1:
        ArduinoSerial.write(b'1')
    if int(i)==2:
        ArduinoSerial.write(b'2')
    if int(i)==3:
        ArduinoSerial.write(b'3')
    if int(i)==4:
        ArduinoSerial.write(b'4')
    if int(i)==5:
        ArduinoSerial.write(b'5')
    if int(i)==6:
        ArduinoSerial.write(b'6')
    if int(i)==7:
        ArduinoSerial.write(b'7')
    if int(i)==8:
        ArduinoSerial.write(b'8')
    if int(i)==9:
        ArduinoSerial.write(b'9')
        
#set the position of printhead origin wrt the arm base origin, for tamara's pdms mold (276.1, -4)     
# arm coord system denoted a , b
#our coord system denoted x , y
x0 = 250 # initial x
y0 = -4 # initial y 
z0 = 50 # initial z position     


#populate the 2D arrays that stores the positions that the arm needs to move to during printing
a_printpath = y_gcode #x positions in arm coord system
b_printpath = x_gcode #y positions in arm coord system

#transform from arm coord system to viewer's coord system with origin x0, y0
#transformation is a-> y and b->x, a 90deg clockwise rotation
xy_printpath = transform.coordinateTransfer(a_printpath, b_printpath, x0, y0,r_stage).T

#move uarm to first position ready for calibration
print('\nMoving to initial position (origin)')
swift.flush_cmd(wait_stop=True)
swift.set_position(xy_printpath[0, 0], xy_printpath[0, 1], 10, speed=3000, timeout=20)
time.sleep(1)
swift.set_position(xy_printpath[0, 0], xy_printpath[0, 1], z_gcode[0], wait=True)

#Calibrate to the desired start position
stepsize=0.25
print("use wasd to control xy arm position, ef for z position and t to terminate")
z_step=0
x_step=0
y_step=0
z_calibrated = z0

while True:
    if keyboard.read_key()==('e'):
        z_step+= stepsize
        #z_calibrated += stepsize
    if keyboard.read_key()==('f'):
        z_step-=stepsize
        #z_calibrated-= stepsize
    if keyboard.read_key()==('a'):
        x_step+= stepsize
    if keyboard.read_key()==('d'):
        x_step-=stepsize
    if keyboard.read_key()==('s'):
        y_step+= stepsize
    if keyboard.read_key()==('w'):
        y_step-=stepsize
    swift.set_position(xy_printpath[0, 0]+x_step, xy_printpath[0, 1]+y_step,z+z_step, wait=True)       
    if keyboard.read_key()==('t'):
        break

start_pos= swift.get_position(wait=True)
start_x = start_pos[0]
start_y = start_pos[1]
start_z = start_pos[2]
print(start_pos)
offset_x = start_x - xy_printpath[0,0]
offset_y = start_y - xy_printpath[0,1]
offset_z = start_z - z_gcode
print(offset_x, offset_y)
#print(xy_printpath)

#set extrusion height to 10mm above glass slide
extrusion_height = 10
#z_calibrated -= 10

#update printpath array to accomodate for offset
for coordinate in xy_printpath:
    coordinate[0]+= offset_x
    coordinate[1]+=offset_y
    #print(coordinate)

#update z array to accomodate for offset
for z in z_gcode:
    z += offset_z 
    z -= extrusion_height
#now create a the printpath to allow the pf127 flow to make good contact and stabilise
#do a straight line in the y direction from y=15 to the xy_printpath start point
a_printpath_stabilise =[15, start_y]
b_printpath_stabilise = [start_x, start_x ]
xy_printpath_stabilise = transform.coordinateTransfer(a_printpath_stabilise, b_printpath_stabilise, x0, y0,r_stage).T

#print values to check
print('stabilise printpath', xy_printpath_stabilise)
print('print path', xy_printpath)

#move away from desired printpath start position to get extrusion going
swift.set_position(xy_printpath_stabilise[0,0], xy_printpath_stabilise[0,1], z_gcode[0], speed=3000, wait=True)

isTerminate = input('Start extruding? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    ArduinoSerial.write(b'5') # Turn off printheads  
    a = swift.get_position(wait=True, timeout=None, callback=None)
    swift.set_position(x=a[0], y=a[1], z=10, wait=True)
    swift.set_position(x=150, y=0, z=10, wait=True)
    swift.set_position(x=105, wait=True)
    swift.set_position(z=20, wait=True)
    swift.set_position(x=115, wait=True)
    swift.set_position(x=105, wait=True)
    sys.exit()

print('\nExtruding...')
swift.set_buzzer(frequency=3000, duration=0.1)
ArduinoSerial.write(b'2') # Turn on printhead 2

isTerminate = input('Start printing pattern? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    ArduinoSerial.write(b'5') # Turn off printheads  
    a = swift.get_position(wait=True, timeout=None, callback=None)
    swift.set_position(x=a[0], y=a[1], z=10, wait=True)
    swift.set_position(x=150, y=0, z=10, wait=True)
    swift.set_position(x=105, wait=True)
    swift.set_position(z=20, wait=True)
    swift.set_position(x=115, wait=True)
    swift.set_position(x=105, wait=True)
    sys.exit()

time.sleep(3)
#print stabilisation line
for x, y in xy_printpath_stabilise:
    swift.set_position(x, y, z_gcode[0],speed=spp, wait=True)
    swift.flush_cmd(wait_stop=True)
#print desired channel pattern
for x, y in xy_printpath:
    swift.set_position(x, y, z_calibrated,speed=spp, wait=True)
    swift.flush_cmd(wait_stop=True)  
time.sleep(2)

ArduinoSerial.write(b'5') # Turn off printheads       
swift.set_buzzer(frequency=3000, duration=0.1)
print('\printing finished')  

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
        


