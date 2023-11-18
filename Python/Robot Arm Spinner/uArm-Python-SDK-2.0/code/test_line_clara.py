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

x_coor_mega = [0, 0, 0, 0, 0, 0]
y_coor_mega = [0, 10, 10, 20, 20, 30]
stepsize=0.2
stage = 2
stage_mega_r = [33, 44.5, 48]
r_stage = stage_mega_r[stage-1]
  
a_cir = 260 #of the printhead from uArm base, mm clara(268.3, 33.1)
b_cir = 28 # y coord of the printhead from uArm base, mm Cassie (276.1, -4)
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
s = 0.1 # Layer height 0.3
z = 10 # Starting z position
sppmm = 1  # printing speed in mm/s
spp = (sppmm - 0.068)/0.043
L1 = 0.4 #0.4 # Thickness of the construct, mm
printingsequence = np.array([1, 1, 1, 1, 1, 1])

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
    k=input()
    if k=="d":
        xyarm_cir[0, 0]=xyarm_cir[0, 0]+stepsize
    if k=="a":
        xyarm_cir[0, 0]=xyarm_cir[0, 0]-stepsize
    if k=="w":
        xyarm_cir[0, 1]=xyarm_cir[0, 1]+stepsize
    if k=="s":
        xyarm_cir[0, 1]=xyarm_cir[0, 1]-stepsize
    if k=="e":
        z=z+stepsize
    if k=="f":
        z=z-stepsize
    if k=="q":
        z=z+10*stepsize
    if k=="g":
        xyarm_cir[0, 1]=xyarm_cir[0, 1]-10*stepsize
        
    swift.set_position(xyarm_cir[0, 0], xyarm_cir[0, 1], z, wait=True)
    if k=="t":
        break
a_cir=[0]
b_cir=[0]
ab = transform_reverse.coordinateTransfer(0,0,xyarm_cir[0, 0], xyarm_cir[0, 1], a_cir, b_cir, r_stage).T
print(ab[0],ab[1])
print(z)
a_cir=ab[0]
b_cir=ab[1]

xyarm_cir = transform.coordinateTransfer(x_coor_mega, y_coor_mega, a_cir, b_cir,44.5).T   
print('\nStart Circle printing')
swift.set_buzzer(frequency=3000, duration=0.1)
ArduinoSerial.write(b'1') # Turn on printhead 3
time.sleep(5)
n = 0
for x, y in xyarm_cir:
    print(n)
    if n >= 1:
        bstring = 'b' + str(printingsequence[n])
        byt = bytes(bstring, 'utf-8')
        ArduinoSerial.write(byt) 
    n += 1
    swift.set_position(x, y, z,speed=spp, wait=True)
    swift.flush_cmd(wait_stop=True)
    
ArduinoSerial.write(b'5') # Turn off printheads   
print('off')    


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