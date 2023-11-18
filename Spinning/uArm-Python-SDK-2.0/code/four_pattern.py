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
ArduinoSerial = serial.Serial('COM4',2400) #COM3 is the port of syringe pump
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
R = 0.7
a_cir = 278.5 # x coord of the printhead from uArm base, mm
b_cir = -1.7 # y coord of the printhead from uArm base, mm


A_eq = 2.6 # Amplitude for  sharp lines
A_eq_2 = 1.5 # Amplitude for sine wave
period = 5.2
B_eq = 2*np.pi/period # Period = 2pi/B
C_eq = 0 # Phase shift, x axis
D_eq =-20# Vertical shift
D_s = 0
n=0

s =-12+n*period/2 #(增减p/2的倍数)
e=7+n*period/2
shape_code=input("which shape do you want to print? s(sine wave),d(diamond),t(triangle),i(icecream)")
if shape_code=="s":
    x1 = np.linspace(s, e, 100)
    y1 = A_eq*np.sin(B_eq*(x1 + C_eq)) + D_eq

    x2 = np.linspace(s, e, 100)
    y2 = -A_eq_2*np.sin(B_eq*(x2 + C_eq)) + D_eq
if shape_code=="d":
    x1 = np.arange(s, e, np.pi/B_eq)
    y1 = A_eq*np.sin(B_eq*(x1 + C_eq)) + D_eq

    x3 = np.arange(s, e, np.pi/B_eq)
    y2 = -A_eq_2*np.sin(B_eq*(x3 + C_eq)) + D_eq
    x2=[]
    for i in x3:
        i=i+0.3
        x2.append(i)
if shape_code=="t":
    x1 = np.arange(s, e, np.pi/B_eq)
    y1 = A_eq*np.sin(B_eq*(x1 + C_eq)) + D_eq

    x3=np.linspace(s, e, 30)
    y2=x3*0+D_eq-0.15
    x2=[]
    for i in x3:
        i=i+0.4
        x2.append(i)
if shape_code=="i":
    x2 = np.arange(s, e, np.pi/B_eq)
    y2 = A_eq*np.sin(B_eq*(x2 + C_eq)) + D_eq

    x3 = np.linspace(s, e, 100)
    y1 = -A_eq_2*np.sin(B_eq*(x3 + C_eq)) + D_eq + D_s
    x1=[]
    for i in x3:
        i=i+0.2
        x1.append(i)

y_cir = [*y1, *y2[::-1]]
x_cir = [*x1, *x2[::-1]]

xyarm_cir = transform.coordinateTransfer(x_cir, y_cir, a_cir, b_cir,48).T     
print('Circle coordinates: ')
for i in range(xyarm_cir.shape[0]):
    print(xyarm_cir[i])
print('')

# Print to std out for checking!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()

# Printing parameters
s = 0.8 # Layer height 0.3
z = 65.7 # Starting z position
spp = 22 # printing speed
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

    
print('\nStart Circle printing')
swift.set_buzzer(frequency=3000, duration=0.1)
ArduinoSerial.write(b'3') # Turn on printhead 3
time.sleep(2)
for z in my_range(z,z-L1,s):
    ArduinoSerial.write(b'3')
    print('\nPrinting a cirlce at %.2f' % z)
    for x, y in xyarm_cir:
        swift.set_position(x, y, z,speed=spp, wait=True)
        swift.flush_cmd(wait_stop=True)  
    
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