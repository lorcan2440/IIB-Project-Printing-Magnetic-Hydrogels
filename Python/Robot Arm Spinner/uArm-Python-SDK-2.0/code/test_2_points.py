# Import modules
import os
import sys
import serial 
import time
import numpy as np
import transform
import transform_reverse
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI
# /home/ieklei/Documents/uArmPython/codes/Yaqi
#import Arduino
ArduinoSerial = serial.Serial('COM4',2400) #COM4 is the port of syringe pump
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
    
# Setting equations
n = 30# cycle number for transversal layers
m = 10 # cycle number for vertical layers
L = 10 # length of the grid
w = 10 # width of the grid
la = 1 # total layer number
x_coor_mega = [0, 0]
y_coor_mega = [6, 0]
stepsize=0.1
stage = 2
stage_mega_r = [33, 44.5, 48]
r_stage = stage_mega_r[stage-1]
  
a_cir = 283.5 #of the printhead from uArm base, mm clara(268.3, 33.1)
b_cir = -4 # y coord of the printhead from uArm base, mm Cassie (276.1, -4)
xyarm_cir = transform.coordinateTransfer(x_coor_mega, y_coor_mega, a_cir, b_cir,44.5).T   
print('Circle coordinates: ')
for i in range(xyarm_cir.shape[0]):
    print(xyarm_cir[i])
print('')
# Print to std out for checking!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()

# Printing parameters
#s = 0.1 # Layer height 0.3
z = 64 # Starting z position
spp = 10 # printing speed
#L1 = 0.4 #0.4 # Thickness of the construct, mm

# Start here-------
print('\nMove to the first circle position')
swift.flush_cmd(wait_stop=True)
swift.set_position(xyarm_cir[0, 0], xyarm_cir[0, 1], 10, speed=3000, timeout=20)
time.sleep(1)
swift.set_position(xyarm_cir[0, 0], xyarm_cir[0, 1], z, wait=True)


print('Circle coordinates: ')
for i in range(xyarm_cir.shape[0]):
    print(xyarm_cir[i])
print('')
# Print to std out for checking!

isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    a = swift.get_position(wait=True, timeout=None, callback=None)
    swift.set_position(x=a[0], y=a[1], z=10, wait=True)
    swift.set_position(x=150, y=0, z=10, wait=True)
    swift.set_position(x=105, wait=True)
    swift.set_position(z=20, wait=True)
    swift.set_position(x=115, wait=True)
    swift.set_position(x=105, wait=True)
    sys.exit()


while True:

    if k=="d":
        xyarm_cir[1, 0]=xyarm_cir[1, 0]+stepsize
    if k=="a":
        xyarm_cir[1, 0]=xyarm_cir[1, 0]-stepsize
    if k=="w":
        xyarm_cir[1, 1]=xyarm_cir[1, 1]+stepsize
    if k=="s":
        xyarm_cir[1, 1]=xyarm_cir[1, 1]-stepsize
    if k=="e":
        z=z+stepsize
    if k=="f":
        z=z-stepsize
    swift.set_position(xyarm_cir[1, 0], xyarm_cir[1, 1], z, wait=True)
    if k=="t":
        p2 = swift.get_position(wait=True, timeout=None, callback=None)
        break
    
a_cir=[0]
b_cir=[0]
ab = transform_reverse.coordinateTransfer(0,0,xyarm_cir[0, 0], xyarm_cir[0, 1], a_cir, b_cir, r_stage).T
print(ab[0],ab[1])
print(z)
a_cir=ab[0]
b_cir=ab[1]
swift.set_position(p2[0], p2[1], 10, speed=3000, timeout=20)
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    a = swift.get_position(wait=True, timeout=None, callback=None)
    swift.set_position(x=a[0], y=a[1], z=10, wait=True)
    swift.set_position(x=150, y=0, z=10, wait=True)
    swift.set_position(x=105, wait=True)
    swift.set_position(z=20, wait=True)
    swift.set_position(x=115, wait=True)
    swift.set_position(x=105, wait=True)
    sys.exit()
swift.set_position(p2[0], p2[1], z, wait=True)
xyarm_cir = [[p2[0],p2[1]],[p1[0],p1[1]]] 
print('\nStart Circle printing')
swift.set_buzzer(frequency=3000, duration=0.1)
ArduinoSerial.write(b'3') # Turn on printhead 3
time.sleep(2)
for x, y in xyarm_cir:
    swift.set_position(x, y, z,speed=spp, wait=True)
    swift.flush_cmd(wait_stop=True) 

time.sleep(4) #delay so final bit can still extrude

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