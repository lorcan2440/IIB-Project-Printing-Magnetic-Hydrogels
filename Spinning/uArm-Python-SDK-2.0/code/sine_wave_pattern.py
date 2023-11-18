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
    
# Setting equations - circle   

a_cir = 282.5  # x coord of the printhead from uArm base, mm
b_cir = -2 # y coord of the printhead from uArm base, mm


A_eq = 0.85 # Amplitude
period = 3.3
B_eq = 2*np.pi/period # Period = 2pi/B
C_eq = 0 # Phase shift, x axis
D_eq = -4 # Vertical shift
p = 0 # adjust the x shift between different vertical shift
m=11
k = 0
while k <= 1:
    if k == 0:
        x1 = np.linspace(2+p, 11+p, 100)
        y1 = A_eq*np.sin(B_eq*(x1 + C_eq)) + D_eq

        x2 = np.linspace(3.2+p, 12.2+p, 100)
        y2 = -A_eq_2*np.sin(B_eq*(x2 + C_eq)) + D_eq  

        x_cir = [*y1, *y2[::-1]]
        y_cir = [*x1, *x2[::-1]]

        xyarm_cir = transform.coordinateTransfer(x_cir, y_cir, a_cir, b_cir,33).T   
    if k == 1:
        x1 = np.linspace(2-m+p, 11-m+p, 100)
        y1 = A_eq*np.sin(B_eq*(x1 + C_eq)) + D_eq

        x2 = np.linspace(3.2-m+p, 12.2-m+p, 100)
        y2 = -A_eq*np.sin(B_eq*(x2 + C_eq)) + D_eq

        x_cir = [*y1, *y2[::-1]]
        y_cir = [*x1, *x2[::-1]]

        xyarm_cir = transform.coordinateTransfer(x_cir, y_cir, a_cir, b_cir,33).T
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

    # Printing parameters
    s = 0.8 # Layer height 0.3
    z = 71 # Starting z position
    spp = 60 # printing speed
    L1 = 0.4 # Thickness of the construct, mm
    n = 0
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
    time.sleep(1)
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
    k = k+1
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