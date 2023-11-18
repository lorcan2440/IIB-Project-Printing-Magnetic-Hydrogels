# Import modules
import os
import sys
import serial 
import time
import numpy as np
import transform
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI

# cd C:\Users\Biointerface\Documents\uArmPython\examples\Jenny
# Import Syringe Pump Arduino
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
    
# Setting
# Square coordinates

x_line = [-10,-10,-5,-5,0,0,5,5,10,10]  # mm
y_line = [-10,10,10,-10,-10,10,10,-10,-10,10]  # mm
x_line_mega = []
y_line_mega = []
for n in np.arange(2000):
    for x, y in zip(x_line, y_line):
        x_line_mega.append(x)
        y_line_mega.append(y)
print(x_line_mega)    
a_line = 282.5  # mm
b_line = 1.5 # mm

'''
# Circle coordinates   
x_line = np.linspace(9,-5,10) # mm
y_line = np.linspace(0,0,10) # mm
a_line = 281  # mm
b_line = 1.5 # mm
'''
r = 33

xyarm_line = transform.coordinateTransfer(x_line_mega, y_line_mega, a_line, b_line, r).T     
print('Line coordinates: ')
for i in range(xyarm_line.shape[0]):
    print(xyarm_line[i])
print('')

# Print to std out for checking!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()
       
# Printing parameters
z = 54


z_line = z # Starting z position of line
sp_line = 100 # uArm speed of line

# Start here-------
print('\nMove to the first line position')
swift.flush_cmd(wait_stop=True)
swift.set_position(xyarm_line[0, 0], xyarm_line[0, 1], 10, speed=3000, timeout=20)
time.sleep(1)
swift.set_position(xyarm_line[0, 0], xyarm_line[0, 1], z_line, wait=True)
swift.flush_cmd(wait_stop=True)

# Print to std out for checking!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()
    
print('\nStart line printing')
swift.set_buzzer(frequency=3000, duration=0.1)
ArduinoSerial.write(b'3')
for x, y in xyarm_line:
    swift.set_position(x, y, z,speed=sp_line, wait=True)
    swift.flush_cmd(wait_stop=True)
    ArduinoSerial.write(b'3')

time.sleep(1)
     
ArduinoSerial.write(b'5')
swift.flush_cmd(wait_stop=True)
time.sleep(1)        
swift.set_buzzer(frequency=3000, duration=0.1)
swift.flush_cmd(wait_stop=True)
print('\nLine printing finished')  

print('\nLowering nozzle to z = 10')
swift.set_position(z=10, speed=3000, wait=True)
print('......')



print('\nVertical line printing finished')  

# Print to std out for checking!
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