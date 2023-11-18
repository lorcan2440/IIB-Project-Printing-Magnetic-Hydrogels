# Import modules
import os
import sys
import serial 
import time
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI

# Import Arduino 
ArduinoSerial = serial.Serial('COM3',2400) #COM3 is the port of syringe pump
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

# My function
def my_range(start, end, step):
    while start >= end:
        yield start
        start = start-step
    
# Coordinate setting
xycoorcir=[[ 249.5,   -0.4],
[ 250.3 ,  -0.8],
[ 251.   , -0.4],
[  251.6,   0.1],
[ 251.9 ,   0.8],
[ 252.   ,  1.5],
[ 251.8  ,  2.2],
[ 251.3  ,  2.8],
[ 250.7  ,  3.3],
[ 249.9  ,  3.5],
[ 249.1  ,  3.5],
[ 248.3  ,  3.3],
[ 247.7  ,  2.8],
[ 247.2  ,  2.2],
[ 247.   ,  1.5],
[ 247.1  ,  0.8],
[  247.4,  0.1],
[ 248.   , -0.4],
[ 248.7  , -0.8],
[ 249.5  , -0.9]]

# Printing parameters
s = 0.3 # Layer height,mm
z = 67 # Starting x position, mm
spp = 40 # printing speed
L = 1 #Thickness of the construct, mm

# Start here--------------------------------------------
print('\nMove to the first circle position')
swift.flush_cmd(wait_stop=True)
swift.set_position(249.5, -0.4, 10, speed= 3000, timeout = 20)
time.sleep(1)
swift.set_position(249.5, -0.4, z, wait = True)

print('\nStart Circle printing')
swift.set_buzzer(frequency=3000, duration=0.1)
ArduinoSerial.write(b'3') # Turn on printhead 3

for z in my_range(z,z-L,s):
    print('\nDrawing a cirlce at %.2f' % z)
    for x, y in xycoorcir:
        swift.set_position(x, y, z,speed=spp, wait=True)
        swift.flush_cmd(wait_stop=True)
        
ArduinoSerial.write(b'5') # Turn off printheads        
swift.set_buzzer(frequency=3000, duration=0.1)
print('\nCircle printing finished')  

print('\nlowering nozzle to z = 10')
swift.set_position(z = 10, speed = 3000, wait = True)

# Always return to the initial position!!! 
print('\nReturn to starting position.(around X95 Y0 Z20)')
swift.set_position(x = 200, y = 0, z=10, wait = True)
swift.flush_cmd()
swift.set_position(x = 150, y = 0, z=10, wait = True)
swift.flush_cmd()
swift.set_position(x =130, y=0, z=10, wait = True)
swift.set_position(z = 20, wait = True)
swift.set_position(x = 115, wait = True)
swift.set_position(x = 105, wait = True)
swift.flush_cmd()
swift.flush_cmd()
swift.set_buzzer(frequency=1000, duration=0.1)
time.sleep(2)
ArduinoSerial.close()