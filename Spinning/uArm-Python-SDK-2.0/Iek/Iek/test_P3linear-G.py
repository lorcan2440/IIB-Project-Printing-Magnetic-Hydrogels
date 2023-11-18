import os
import sys
import serial 
import time
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI

# My modules
import transform

# Import Arduino
ArduinoSerial = serial.Serial('COM3',2400)
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

# my utilities

def my_range(start, end, step):
    while start >= end:
        yield start
        start = start-step


# Load Gcodefile:///home/ieklei/Documents/uArmPython/examples/api/single/v3-printer/gcode-transform/test_gcode_hand.py

#40 60 80
spp =10 # Printing speed
spnp = 1000  # Not printing speed 
#66.5
# 63 for 25G
Z0 = 62
X0 = 250-32
Y0 = 1.5

# Start here-------
print('\nMove to the first circle position')
swift.flush_cmd(wait_stop=True)
swift.set_position(X0, Y0, 10, speed=3000, timeout=20)
time.sleep(1)
swift.set_position(X0, Y0, Z0, wait=True)

time.sleep(3)
# Print to std out for checking!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()
    
print('\nStart Circle printing')
swift.set_buzzer(frequency=3000, duration=0.1)
ArduinoSerial.write(b'3')
time.sleep(2)
n = 1
f = 0.3
for n in range (1,42):
    #swift.set_position(X0+n, Y0, Z0, speed=(1+0.8*n*f)*spp, wait=True)
    #spp-(n/40)*(spp-25)
    swift.set_position(X0+n, Y0, Z0, speed=spp+(n/42)*0*spp, wait=True)
    swift.flush_cmd()
    
ArduinoSerial.write(b'5')


swift.set_buzzer(frequency=3000, duration=0.1)
print('\nCircle printing finished')  

print('\nLowering nozzle to z = 10')
swift.set_position(z=10, speed=500, wait=True)
print('......')

isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()
    
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