# Import modules
import os
import sys
import serial 
import time
import numpy as np
import transform
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI
# /home/ieklei/Documents/uArmPython/codes/Yaqi
# Import Arduino
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
a_org =5
n = 6# cycle number for transversal layers
m = 20 # cycle number for vertical layers
L = 2 # width of the grid
w = 2# length of the grid
la = 1 # total layer number
b_org =6#horizental
x_coor_mega = [a_org, a_org]
y_coor_mega = [b_org, b_org]
x_coor_2_mega = []
y_coor_2_mega = []

for num in range(n):
    if num == 0:
        b = b_org
    if num > 0:
        b = b + L/n
    
    x_coord = [a_org, a_org, a_org+w, a_org+w, a_org]
    y_coord = [b, b+L/(2*n), b+L/(2*n), b+L/n, b+L/n]
    
    for i, j in zip(x_coord, y_coord):
        x_coor_mega.append(i)
        y_coor_mega.append(j)
#x_coor_mega.append(a_org)
#x_coor_mega.append(a_org+w)
#x_coor_mega.append(a_org+w)
#x_coor_mega.append(a_org)
#y_coor_mega.append(b_org)
#y_coor_mega.append(b_org)
#y_coor_mega.append(b_org+L) 
#y_coor_mega.append(b_org+L)

for num in range(m):
    if num == 0:
        a = a_org
    if num > 0:
        a = a + w/m
    b = b_org
        
    x_coord = [a, a, a+w/(2*m), a+w/(2*m), a+w/m]
    y_coord = [b+L, b, b, b+L, b+L]
    
    for i, j in zip(x_coord, y_coord):
        x_coor_2_mega.append(i)
        y_coor_2_mega.append(j)
x_coor_2_mega.append(a_org+w)
x_coor_2_mega.append(a_org+w)
x_coor_2_mega.append(a_org)
y_coor_2_mega.append(b_org+L)
y_coor_2_mega.append(b_org)
y_coor_2_mega.append(b_org) 
  
  
a_cir = 279 #of the printhead from uArm base, mm
b_cir = -3 # y coord of the printhead from uArm base, mm
xyarm_cir = transform.coordinateTransfer(x_coor_mega, y_coor_mega, a_cir, b_cir,33).T 
xyarm_cir_2 = transform.coordinateTransfer(x_coor_2_mega, y_coor_2_mega, a_cir, b_cir,33).T     
print('Circle coordinates: ')
for i in range(xyarm_cir.shape[0]):
    print(xyarm_cir[i])
for i in range(xyarm_cir_2.shape[0]):
    print(xyarm_cir_2[i])
print('')
# Print to std out for checking!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()

# Printing parameters
s = 0.1 # Layer height 0.3
z = 70.78# Starting z position
spp = 80 # printing speed （120 for gelMa network)
L1 = 0.4 # Thickness of the construct, mm

# Start here-------
print('\nMove to the first circle position')
swift.flush_cmd(wait_stop=True)
swift.set_position(xyarm_cir[0, 0], xyarm_cir[0, 1], 10, speed=3000, timeout=20)
time.sleep(1)
swift.set_position(xyarm_cir[0, 0], xyarm_cir[0, 1], z, wait=True)


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

layer_number = 1
print('\nStart Circle printing')
swift.set_buzzer(frequency=3000, duration=0.1)
ArduinoSerial.write(b'3') # Turn on printhead 3
while layer_number <= la:
    if layer_number == 1:
        time.sleep(3)
    z = z-s*(layer_number-1)
    if layer_number%2 != 0:   
        ArduinoSerial.write(b'3')
        print('\nPrinting a cirlce at %.2f' % z)
        for x, y in xyarm_cir:
            swift.set_position(x, y, z,speed=spp, wait=True)
            swift.flush_cmd(wait_stop=True) 
    if layer_number%2 == 0:
        ArduinoSerial.write(b'3')
        print('\nPrinting a cirlce at %.2f' % z)
        for x, y in xyarm_cir_2:
            swift.set_position(x, y, z,speed=spp, wait=True)
            swift.flush_cmd(wait_stop=True) 
    layer_number = layer_number+1
    print (layer_number)
    
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