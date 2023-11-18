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
ArduinoSerial = serial.Serial('COM3',2400) #COM3 is the port of the syringe pump
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
    

# import spiral equations   
a = 0.3
b = 0.3
Theta = np.linspace( 2 * 2.64 * np.pi,0, 40)[:-1]
R = a + b*Theta
x_spi = R * np.cos(Theta)
y_spi = R * np.sin(Theta)
z_spi = np.linspace(0,4.44,40)
a_spi = 282.5  # mm
b_spi = 1.5 # mm
xyarm_spi = transform.coordinateTransfer(x_spi, y_spi, a_spi, b_spi).T  
   
print('Circle coordinates: ')
for i in range(xyarm_spi.shape[0]):
    print(xyarm_spi[i])
print('')

# Print to std out for checking!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()

# Printing parameters
s = 0.3 # Layer height
z1 = 63 # Starting z position of material 1
spp = 10 # uArm speed of material 1

# Start here-------
print('\nMove to the first circle position')
swift.flush_cmd(wait_stop=True)
swift.set_position(xyarm_spi[0, 0], xyarm_spi[0, 1], 10, speed=3000, timeout=20)
time.sleep(1)
swift.set_position(xyarm_spi[0, 0], xyarm_spi[0, 1], z1, wait=True)


# Print to std out for checking!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()

    
print('\nStart printing')
swift.set_buzzer(frequency=3000, duration=0.1)
ArduinoSerial.write(b'3') # To turn on printhead 3
n = 1
z = z1
time.sleep(1)
for x, y in xyarm_spi:
    swift.set_position(x, y, z,speed=10, wait=True)
    z = z1-4.44*n/40
    n = n + 1
    swift.flush_cmd(wait_stop=True)
    
ArduinoSerial.write(b'5') # To turn off all printheads  
swift.set_buzzer(frequency=3000, duration=0.1)
print('\nPrinting finished')  

print('\nLowering nozzle to z = 10')
swift.set_position(z=10, speed=3000, wait=True)
print('......')

isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()

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