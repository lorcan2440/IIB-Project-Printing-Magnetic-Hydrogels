# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 22:57:50 2022

@author: Cassie chan
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
        
# Printing parameters
spp = 35 # printing speed
#n = 0
r_stage=44.5 #petridish radius
delaytime=20000 #corresponds to extrusion speed
length=len(str(delaytime))

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
y0 = 5 # initial y 
z0 = 60 # initial z position

#circle equation
R =5
k=2*R #horizontal


Theta1 = np.linspace(0,np.pi, 100)
x1 = R* np.cos(Theta1 + np.pi)+k
y1 = R* np.sin(Theta1 + np.pi)

Theta2 = np.linspace(np.pi, 2*np.pi, 100)
x2 = R* np.cos(Theta2 + np.pi)+k
y2 = R* np.sin(Theta2 + np.pi)

#populate the 2D arrays that stores the positions that the arm needs to move to during printing
#sine
a_printpath = [*y1] #x positions in arm coord system
b_printpath = [*x1] #y positions in arm coord system
#straight line at end
a_printpath.append(0)
b_printpath.append(20)
#straight line at beginning
a_printpath.insert(0, 0)
a_printpath.insert(1, 0)
b_printpath.insert(0, 0)
b_printpath.insert(1, 3)

for y in y2:
    a_printpath.append(y)

for x in x2:
    b_printpath.append(x)

a_printpath.append(0)
b_printpath.append(-2)

#transform from arm coord system to viewer's coord system with origin x0, y0
#transformation is a-> y and b->x, a 90deg clockwise rotation
xy_printpath = transform.coordinateTransfer(a_printpath, b_printpath, x0, y0,r_stage).T


#move uarm to first position ready for calibration
print('\nMoving to initial position (origin)')
swift.flush_cmd(wait_stop=True)
swift.set_position(xy_printpath[0, 0], xy_printpath[0, 1], 10, speed=3000, timeout=20)
time.sleep(1)
swift.set_position(xy_printpath[0, 0], xy_printpath[0, 1], z0, wait=True)

#CALIBRATION
stepsize=0.25
#get user to input top left corner of slide
print('Move to top left corner of slide. Use wasd to control xy arm position, ef for z position and r to register')
z_step=0
x_step=0
y_step=0
z_calibrated = z0

while True:
    if keyboard.read_key()==('e'):
        z_step+= stepsize
        z_calibrated += stepsize
    if keyboard.read_key()==('f'):
        z_step-=stepsize
        z_calibrated-= stepsize
    if keyboard.read_key()==('a'):
        x_step+= stepsize
    if keyboard.read_key()==('d'):
        x_step-=stepsize
    if keyboard.read_key()==('s'):
        y_step+= stepsize
    if keyboard.read_key()==('w'):
        y_step-=stepsize
    swift.set_position(xy_printpath[0, 0]+x_step, xy_printpath[0, 1]+y_step,z0+z_step, wait=True)       
    if keyboard.read_key()==('r'):
        break
top_left= swift.get_position(wait=True) #position of the top left corner of slide

print('Move to bottom left corner of slide. Use wasd to control xy arm position, ef for z position and r to register')
z_step=0
x_step=0
y_step=0
z_calibrated = z0

while True:
    if keyboard.read_key()==('e'):
        z_step+= stepsize
        z_calibrated += stepsize
    if keyboard.read_key()==('f'):
        z_step-=stepsize
        z_calibrated-= stepsize
    if keyboard.read_key()==('a'):
        x_step+= stepsize
    if keyboard.read_key()==('d'):
        x_step-=stepsize
    if keyboard.read_key()==('s'):
        y_step+= stepsize
    if keyboard.read_key()==('w'):
        y_step-=stepsize
    swift.set_position(top_left[0]+x_step, top_left[1]+y_step,top_left[2]+z_step, wait=True)       
    if keyboard.read_key()==('r'):
        break
bottom_left= swift.get_position(wait=True)

print('top left:', top_left, 'bottom left:', bottom_left)

start_pos = np.zeros(3)
for i in range(3):
    start_pos[i]= (top_left[i]+bottom_left[i])/2
print('start position:', start_pos)
start_x = start_pos[0]
start_y = start_pos[1]
z_calibrated = start_pos[2]
offset_x = start_x - xy_printpath[0,0]
offset_y = start_y - xy_printpath[0,1]
print('offsets:', offset_x, offset_y)

#move z position to 10mm above glass slide
z_calibrated -= 1.5

#update printpath array to accomodate for offset
for coordinate in xy_printpath:
    coordinate[0]+= offset_x
    coordinate[1]+=offset_y
    #print(coordinate)


#print values to check
#print('print path', xy_printpath)

#move away from desired printpath start position to get extrusion going
swift.set_position(xy_printpath[0,0]-5, xy_printpath[0,1]-10, z_calibrated, speed=3000, wait=True)

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

#move to starting position
swift.set_position(xy_printpath[0,0]-5, xy_printpath[0,1], z_calibrated, speed=spp, wait=True)    
swift.set_position(xy_printpath[0,0], xy_printpath[0,1], z_calibrated,speed=spp, wait=True)

swift.set_buzzer(frequency=1500, duration=0.1)
print('\nPrinting Pattern...')
for x, y in xy_printpath:
    swift.set_position(x, y, z_calibrated,speed=spp, wait=True)
    swift.flush_cmd(wait_stop=True)  
time.sleep(1)

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
        

