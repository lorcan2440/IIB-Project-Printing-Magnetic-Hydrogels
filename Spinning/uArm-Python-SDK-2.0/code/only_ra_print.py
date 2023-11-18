# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 21:02:16 2022

@author: printer
"""

# Import modules
import os
import sys

import time
import keyboard
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI


# Import uArm
swift = SwiftAPI(filters={'hwid': 'USB VID:PID=2341:0042'})
swift.waiting_ready(timeout=3)
device_info = swift.get_device_info()
print(device_info)
firmware_version = device_info['firmware_version']
if firmware_version and not firmware_version.startswith(('0.', '1.', '2.', '3.')):
    swift.set_speed_factor(0.0005)
swift.set_mode(0)

# My function
def my_range(start, end, step):
    while start >= end:
        yield start
        start = start-step
        
a = swift.get_position(wait=True, timeout=None, callback=None)
z=20
while True:
    stepsize=float(input('stepsize'))
    print("use wasd to control xy position, ef for Z position and q to quit")
    while True:
        if keyboard.read_key()==('a'):
            a[0]=a[0]+stepsize
        if keyboard.read_key()==('d'):
            a[0]=a[0]-stepsize
        if keyboard.read_key()==('s'):
            a[1]=a[1]+stepsize
        if keyboard.read_key()==('w'):
            a[1]=a[1]-stepsize
        if keyboard.read_key()==('e'):
            z=z+stepsize
        if keyboard.read_key()==('f'):
            z=z-stepsize
        swift.set_position(a[0], a[1],z, wait=True)
        if keyboard.read_key()==('q'):
            break  
    print('start to print? press y')
    if keyboard.read_key()==('y'):
        break
        
# Setting equations
a_org = a[0]
n = 10
L = 10
w = 10
b_org = a[1]
x_coor_mega = [a_org, a_org]
y_coor_mega = [b_org, b_org]

for num in range(n):
    if num == 0:
        b = b_org
    if num > 0:
        b = b + L/n
    
    x_coord = [a_org, a_org, a_org+w, a_org+w, a_org]
    y_coord = [b, b+L/(2*n), b+L/(2*n), b+L/n, b+L/n]
    
    for i, j in zip(x_coord, y_coord):
        x_coor_mega.append(i)
        y_coor_mega.append(j)
 

  
print('Circle coordinates: ')
for i in range(len(x_coor_mega)):
    print(x_coor_mega[i])
for i in range(len(y_coor_mega)):
    print(y_coor_mega[i])
print('')

# Print to std out for checking!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()

# Printing parameters
s = 0.15 # Layer height 0.3
spp = 120 # printing speed
L1 = 0.4 # Thickness of the construct, mm

# Start here-------
print('\nMove to the first circle position')
swift.flush_cmd(wait_stop=True)
swift.set_position(x_coor_mega[0], y_coor_mega[0], z, speed=3000, timeout=20)
time.sleep(1)
swift.set_position(x_coor_mega[0], y_coor_mega[0], z, wait=True)


# Print to std out for checking!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()

layer_number = 1
print('\nStart Circle printing')
swift.set_buzzer(frequency=3000, duration=0.1)
i=0

while i<= len(x_coor_mega)-1 :
    x=x_coor_mega[i]
    y=y_coor_mega[i]
    swift.set_position(x, y, z,speed=spp, wait=True)
    i=i+1
    swift.flush_cmd(wait_stop=True) 
    
swift.set_buzzer(frequency=3000, duration=0.1)
print('\nCircle printing finished')  

print('\nLowering nozzle to z = 10')
swift.set_position(z=60, speed=3000, wait=True)
print('......')

# Always return to the initial position!!! 
print('\nReturn to starting position.(around X95 Y0 Z20)')

swift.set_position(x=95, y=0, z=60, wait=True)
swift.set_position(x=95, y=0, z=20, wait=True)
swift.flush_cmd()
swift.flush_cmd()
swift.set_buzzer(frequency=1000, duration=0.1)
time.sleep(2)

