# Import modules
import os
import sys
import serial 
import time
import numpy as np
import transform
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
    
# Setting equations - circle   
R = 5
Theta = np.linspace(0, 2 * np.pi, 20)[:-1]
x_cir = R * np.cos(Theta)
y_cir = R * np.sin(Theta)
a_cir = 282.5  # x coord of the printhead from uArm base, mm
b_cir = 1.5 # y coord of the printhead from uArm base, mm
xyarm_cir = transform.coordinateTransfer(x_cir, y_cir, a_cir, b_cir,33).T     
print('Circle coordinates: ')
for i in range(xyarm_cir.shape[0]):
    print(xyarm_cir[i])
print('')

# Print to std out for checking!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()

# Printing parameters
s = 0.3 # Layer height 0.3
z = 63.5 # Starting z position 72
spp = 10 # printing speed
L1 = 4 # Thickness of the construct, mm
n = -1
# Start here-------
print('\nMove to the first circle position')
swift.flush_cmd(wait_stop=True)
swift.set_position(xyarm_cir[-1, 0], xyarm_cir[-1, 1], 10, speed=3000, timeout=20)
time.sleep(1)
swift.set_position(xyarm_cir[-1, 0], xyarm_cir[-1, 1], z, wait=True)


# Print to std out for checking!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()

    
print('\nStart Circle printing')
swift.set_buzzer(frequency=3000, duration=0.1)
ArduinoSerial.write(b'3') # Turn on printhead 3
for z in my_range(z,z-L1,s):
    ArduinoSerial.write(b'3')
    print('\nPrinting a cirlce at %.2f' % z)
    for x, y in xyarm_cir:
        swift.set_position(x, y, z,speed=spp, wait=True)
        swift.flush_cmd(wait_stop=True)  
    if (n % 2) == 0:
        ArduinoSerial.write(b'5')
        swift.set_position(z=10, speed=1000, wait=True)
        swift.set_position(150, 70, 10, wait=True)
        isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
        if isTerminate == 'n':
            sys.exit()
        swift.set_position(x, y, 10, wait=True)
        swift.set_position(x, y, z, wait=True)
    n = n+1
ArduinoSerial.write(b'5') # Turn off printheads       
swift.set_buzzer(frequency=3000, duration=0.1)
print('\nCircle printing finished')  

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