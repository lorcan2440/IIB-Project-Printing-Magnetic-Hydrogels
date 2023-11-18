# -*- coding: utf-8 -*-
"""
Created on Thu Jun  9 18:44:54 2022

@author: printer
"""

import os
import sys
import serial 
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI
import keyboard 


#import Arduino
ArduinoSerial = serial.Serial('COM5',2400) #COM5 is the port for arduino 
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
channel_length = 5
# X-Y coordinates transformation
a = swift.set_position(285, -1,10, wait=True)
a = swift.set_position(285, -1,65, wait=True)
while True:
    stepsize=float(input('Hi Adash, what is the stepsize you want?'))
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
            a[2]=a[2]+stepsize
        if keyboard.read_key()==('f'):
            a[2]=a[2]-stepsize
        swift.set_position(a[0], a[1],a[2], wait=True)
        if keyboard.read_key()==('q'):
            break
print('\nStart line printing')
swift.set_buzzer(frequency=3000, duration=0.1)
ArduinoSerial.write(b'3') # Turn on printhead 3
time.sleep(3) 
swift.set_position(a[0]+channel_length, a[1],a[2], wait=True)
          
ArduinoSerial.write(b'5') # Turn off printheads       
swift.set_buzzer(frequency=3000, duration=0.1)
print('\nEquation printing finished')  

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

print('Printing done!')
