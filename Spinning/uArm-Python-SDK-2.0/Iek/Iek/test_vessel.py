# Import modules
import os
import sys
import serial 
import time
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI

# Import my modules
import transform 
import gcodemod

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

# Function
def my_range(start, end, step):
    while start >= end:
        yield start
        start = start-step

# Load Gcode
spp = 10 # Printing speed
spnp = 1000  # Not printing speed 
Z0 = 73 # starting z position
offset = [0, 0, Z0] # Setting as [0,0,Z0] means printing at the central point (a_gcode,b_gcde) of the stage at Z0
bigCoor = gcodemod.read(r"C:\Users\Biointerface\Documents\uArmPython\examples\Iek\Part3-04.txt", offset) # Import gcode
x_gcode = bigCoor[:, 0] # Import x coord from gcode file
y_gcode = bigCoor[:, 1] # Import y coord from gcode file
z_gcode = bigCoor[:, 2] # Import z coord from gcode file
e_gcode = bigCoor[:, 3]  # Import extrusion information from gcode file 


# X-Y coordinates transformation
a_gcode = 282.5  # x coord of the printhead from uArm base, mm 
b_gcode = 1.5 # y coord of the printhead from uArm base, mm
# Transfrom printing coordinates to uArm coordinates, same ref point.
xyarm_gcode = transform.coordinateTransfer(x_gcode, y_gcode, a_gcode, b_gcode,33).T
zarm_gcode = np.copy(z_gcode)  # z position, do no transform z coordinates
print('Gcode coordinates: ')
for i in range(xyarm_gcode.shape[0]):
    print(np.append(xyarm_gcode[i], zarm_gcode[i]))
print('')

# Print to std out for checking gcode!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()

# Start here-------
print('\nMove to the first circle position')
swift.flush_cmd(wait_stop=True)
swift.set_position(xyarm_gcode[0, 0], xyarm_gcode[0, 1], 10, speed=3000, timeout=20)
time.sleep(1)
swift.set_position(xyarm_gcode[0, 0], xyarm_gcode[0, 1], zarm_gcode[0], wait=True)


# Print to std out for checking Z0!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()
    
print('\nStart gcode printing')
swift.set_buzzer(frequency=3000, duration=0.1)
for n, etem in enumerate(e_gcode):
    if etem == 1: # printing
         ArduinoSerial.write(b'3') # Turn on printhead 3
         swift.set_position(xyarm_gcode[n, 0], xyarm_gcode[n, 1], zarm_gcode[n],
                speed=spp, wait=True)
    elif etem == 0: # stop printing
        ArduinoSerial.write(b'5') # Turn off printheads
        swift.set_position(xyarm_gcode[n, 0], xyarm_gcode[n, 1], zarm_gcode[n],
                speed=spnp, wait=True)
    swift.flush_cmd()

    
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