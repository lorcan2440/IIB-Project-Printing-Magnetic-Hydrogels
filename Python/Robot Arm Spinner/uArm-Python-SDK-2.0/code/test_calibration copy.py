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
offset = [0, 0, Z0] # Setting as [0,0,Z0] means printing at the central point (a_gcode,b_gcde) of the stage at Z0
printhead = 5
stage = 4 #1 Small, 2 Large, 3 microscope slide
stepsize = 1

bigCoor = gcodemod.read(r"C:\Users\49250\Documents\uArm-Python-SDK-2.0\code\sbox.txt", offset) # Import gcode

x_gcode = bigCoor[:, 0] # Import x coord from gcode file
y_gcode = bigCoor[:, 1] # Import y coord from gcode file
z_gcode = bigCoor[:, 2] # Import z coord from gcode file
e_gcode = bigCoor[:, 3]  # Import extrusion information from gcode file 


# X-Y coordinates transformation
ab = [[280.6,70.5], [280.5,0.1], [280,-74],[250,-4]] #Calibrated printhead 2,3,4 a,b coordinates
stage_mega_r = [33, 44.5, 48,38]
a_gcode = ab[printhead-2][0] # x coord of the printhead from uArm base, mm 
b_gcode = ab[printhead-2][1] # y coord of the printhead from uArm base, mm
r_stage = stage_mega_r[stage-1]

x_cir = [0]
y_cir = [0]
# Transfrom printing coordinates to uArm coordinates, same ref point.
xyarm_gcode = transform.coordinateTransfer(x_cir, y_cir, a_gcode, b_gcode, r_stage).T

# set arduino


# Print to std out for checking gcode!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()

# Start here-------
print('\nMove to the first circle position')
swift.flush_cmd(wait_stop=True)
swift.set_position(xyarm_gcode[0, 0], xyarm_gcode[0, 1], 10, speed=3000, timeout=20)
print (xyarm_gcode[0, 0]+stage_mega_r[0], xyarm_gcode[0, 1])
time.sleep(1)
swift.set_position(xyarm_gcode[0, 0], xyarm_gcode[0, 1], Z0, wait=True)
print("use wasd to control xy position, ef for Z position and t to terminate")
while True:
    if keyboard.read_key()==('d'):
        xyarm_gcode[0, 0]=xyarm_gcode[0, 0]+stepsize
    if keyboard.read_key()==('a'):
        xyarm_gcode[0, 0]=xyarm_gcode[0, 0]-stepsize
    if keyboard.read_key()==('w'):
        xyarm_gcode[0, 1]=xyarm_gcode[0, 1]+stepsize
    if keyboard.read_key()==('s'):
        xyarm_gcode[0, 1]=xyarm_gcode[0, 1]-stepsize
    if keyboard.read_key()==('e'):
        Z0=Z0+stepsize
    if keyboard.read_key()==('f'):
        Z0=Z0-stepsize
    swift.set_position(xyarm_gcode[0, 0], xyarm_gcode[0, 1], Z0, wait=True)
    if keyboard.read_key()==('q'):
        break
a_cir=[0]
b_cir=[0]
ab = transform_reverse.coordinateTransfer(0,0,xyarm_gcode[0, 0], xyarm_gcode[0, 1], a_cir, b_cir, r_stage).T
print(ab[0],ab[1])#calibrated a b cordinates
# Print to std out for checking Z0!
isTerminate = input('press n to terminate ')
if isTerminate == 'n':
    a = swift.get_position(wait=True, timeout=None, callback=None)
    swift.set_position(x=a[0], y=a[1], z=10, wait=True)
    swift.set_position(x=150, y=0, z=10, wait=True)
    swift.set_position(x=105, wait=True)
    swift.set_position(z=20, wait=True)
    swift.set_position(x=115, wait=True)
    swift.set_position(x=105, wait=True)
    sys.exit()

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