# Import modules
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
import transform_reverse

# Import Arduino
ArduinoSerial = serial.Serial('COM5',2400) #COM3 is the port of syringe pump
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
spp = 15  # Printing speed
spnp = 1000  # Not printing speed 
Z0 = 58 # starting z position
stepsize=0.2
line_length=10
a=[230,0]
swift.set_position(230, 0, Z0, wait=True)

print("use wasd to control xy position, ef for Z position and t to terminate")
while True:
    if keyboard.read_key()==('d'):
        a[0]+=stepsize
    if keyboard.read_key()==('a'):
        a[0]-=stepsize
    if keyboard.read_key()==('w'):
        a[1]+=stepsize
    if keyboard.read_key()==('s'):
        a[1]-=stepsize
    if keyboard.read_key()==('e'):
        Z0=Z0+stepsize
    if keyboard.read_key()==('f'):
        Z0=Z0-stepsize
    swift.set_position(a[0], a[1], Z0, wait=True)
    if keyboard.read_key()==('q'):
        break

print(a)




# Start here-------
ArduinoSerial.write(b'2')
isTerminate = input('type any key to start printing if the extrusion is OK')
swift.set_position(line_length+a[0], a[1], Z0, speed=spp,wait=True)
ArduinoSerial.write(b'5')

print('finished first line, move to the start pos for second line printing')
swift.set_position(line_length+a[0], a[1], 10, speed=spnp,wait=True)
swift.set_position(a[0], a[1], 10, speed=spnp,wait=True)
swift.set_position(a[0], a[1], Z0-0.2, speed=spnp,wait=True)

print('change needle')
isTerminate = input('type any key to continue if needle changed')
ArduinoSerial.write(b'1')
isTerminate = input('type any key to start printing if the extrusion is OK')
swift.set_position(line_length+a[0], a[1], Z0, speed=spp,wait=True)
ArduinoSerial.write(b'5')


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