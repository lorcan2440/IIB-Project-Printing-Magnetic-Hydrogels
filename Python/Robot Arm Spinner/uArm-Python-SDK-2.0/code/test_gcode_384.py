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

# Function
def my_range(start, end, step):
    while start >= end:
        yield start
        start = start-step

# Load Gcode
spp = 800  # Printing speed
spnp = 1000  # Not printing speed 
Z0 = 82 # starting z position
z=11 #z shift from top to plate 
#offset = [-5, -5, Z0] # Setting as [0,0,Z0] means printing at the central point (a_gcode,b_gcde) of the stage at Z0
printhead = 5 #printhead for portabel one
stage = 3 #1 Small, 2 Large, 384 well plate

num=0
x_o=0
y_o=0

# X-Y coordinates transformation
ab = [[282.5,76], [282.5,1.5], [280,-74], [269,-5]] #Calibrated printhead 2,3,4 a,b coordinates
stage_mega_r = [33, 44.5, 78]
a_gcode = ab[printhead-2][0] # x coord of the printhead from uArm base, mm 
b_gcode = ab[printhead-2][1] # y coord of the printhead from uArm base, mm
r_stage = stage_mega_r[stage-1]
swift.set_position(a_gcode-r_stage, b_gcode, 10, speed=3000, timeout=20)
swift.set_position(a_gcode-r_stage, b_gcode, Z0, speed=3000, timeout=20)

iscalibration = input('Need calibration? Please type y to calibration, or any other key to skip: ')
if iscalibration == 'y':
         
    while True:
        z_s=float(input('z_shift'))
        Z0+=z_s
        swift.set_position(a_gcode-r_stage, b_gcode, Z0, speed=3000, timeout=20)
        isTerminate = input('Continue? Please type y to process forward: ')
        if isTerminate == 'y':
             break
    
    while True:
        y_s=float(input('x_shift'))
        a_gcode+=y_s
        swift.set_position(a_gcode-r_stage, b_gcode, Z0, speed=3000, timeout=20)
        isTerminate = input('Continue? Please type y to process forward: ')
        if isTerminate == 'y':
            break 
        
    while True:
        x_s=float(input('y_shift'))
        b_gcode+=x_s
        swift.set_position(a_gcode-r_stage, b_gcode, Z0, speed=3000, timeout=20)
        isTerminate = input('Continue? Please type y to process forward: ')
        if isTerminate == 'y':
            break 


x_f=[0]
y_f=[0]
xa=x_f[0]
ya=y_f[0]
xy_gcode = transform.coordinateTransfer(x_f, y_f, a_gcode, b_gcode, r_stage).T
# move to the center of the first well.
swift.set_position(xy_gcode[0,0], xy_gcode[0,1], 10, speed=3000, timeout=20)
swift.set_position(xy_gcode[0,0], xy_gcode[0,1], Z0, speed=3000, timeout=20)

print('adjust the printhead position to the start row')    

while True:
    if keyboard.read_key()==('e'):
        ArduinoSerial.write(b'5')
    if keyboard.read_key()==('f'):
        ArduinoSerial.write(b'4')
    if keyboard.read_key()==('s'):
        ArduinoSerial.write(b'8')
    if keyboard.read_key()==('q'):
        break

i=0
s=0    
ii=int(input('how many structures in one row'))
ss=int(input('how many rows to be printed'))
c=0
#a=[[-0.5, -51.4, 82], [-0.5, -46.9, 82], [-0.2, -42.4, 82], [-0.2, -37.9, 82], [-0.2, -33.6, 82], [-0.2, -29.200000000000003, 82], [-0.2, -24.900000000000002, 82], [-0.2, -20.5, 82], [-0.1, -16.1, 82], [-0.1, -11.700000000000001, 82], [-0.1, -7.100000000000001, 82], [-0.1, -2.6000000000000014, 82], [0.2, 1.8999999999999986, 82], [0.2, 6.399999999999999, 82], [0.4, 10.899999999999999, 82], [0.6000000000000001, 15.2, 82], [0.6000000000000001, 19.6, 82], [0.6000000000000001, 24.1, 82], [0.9000000000000001, 28.6, 82], [0.9000000000000001, 32.800000000000004, 82], [0.9000000000000001, 37.300000000000004, 82], [0.9000000000000001, 41.7, 82], [1.1, 46.300000000000004, 82], [1.1, 50.800000000000004, 82]]
a=[[-1.0, -51.5, 82.0], [-1.0, -47.0, 82.0], [-1.0, -42.5, 82.0], [-1.0, -38.0, 82.0], [-1.0, -33.5, 82.0], [-1.0, -29.0, 82.0], [-1.0, -24.7, 82.0], [-1.0, -20.2, 82.0], [-1.0, -15.7, 82.0], [0.0, -11.2, 82.0], [0.0, -6.699999999999999, 82.0], [0.0, -2.499999999999999, 82.0], [0.0, 2.000000000000001, 82.0], [0.0, 6.500000000000001, 82.0], [0.2, 11.0, 82.0], [0.4, 15.5, 82.0], [0.6000000000000001, 19.7, 82.0], [0.8, 24.2, 82.0], [1.1, 28.4, 82.0], [1.4000000000000001, 32.9, 82.0], [1.4000000000000001, 37.4, 82.0], [1.7000000000000002, 41.9, 82.0], [2.0, 46.4, 82.0], [2.0, 50.6, 82.0]]
b=[[0.0, -49.7, 82], [0.0, -45.2, 82], [0.0, -40.7, 82], [0.5, -36.2, 82], [0.8, -31.700000000000003, 82], [0.8, -27.200000000000003, 82], [0.8, -23.000000000000004, 82], [0.8, -18.5, 82], [1.3, -14.0, 82], [2.1, -9.5, 82], [2.1, -5.0, 82], [2.1, -0.5, 82], [2.1, 4.0, 82], [2.3000000000000003, 8.5, 82], [2.9000000000000004, 13.0, 82], [3.2, 17.5, 82], [3.5, 21.8, 82], [3.8, 26.3, 82], [3.8, 30.8, 82], [4.1, 35.0, 82], [4.3999999999999995, 39.5, 82], [4.999999999999999, 44.0, 82], [4.999999999999999, 48.5, 82], [4.999999999999999, 53.0, 82]]
for k in a:
    k[2]=Z0+z
for e in b:
    e[2]=Z0+z
while c<=ii*ss-2:
    if i<=ii-1:
        if s<=7:
            offset=a[i]
        else:
            offset=b[i]
        
        i+=1
    else:
        if i<2*ii-1:
            s+=1
            if i==ii:
                ArduinoSerial.write(b'2') 
                time.sleep(0.4)
                ArduinoSerial.write(b'8')
            if s<=7:
                offset=a[2*ii-i-1] 
            else:
                offset=b[2*ii-i-1] 
            i+=1
        if i==2*ii-1:
            s=s+1
            if s<=7:
                offset=a[0]
            else:
                offset=b[0]
            i=0
            
            


                    
    bigCoor = gcodemod.read(r"C:\Users\49250\Documents\uArm-Python-SDK-2.0\code\sbox.txt", offset) # Import gcode
    c+=1
    
    x_gcode = bigCoor[:, 0] # Import x coord from gcode file
    y_gcode = bigCoor[:, 1] # Import y coord from gcode file
    z_gcode = bigCoor[:, 2] # Import z coord from gcode file
    e_gcode = bigCoor[:, 3]  # Import extrusion information from gcode file 



    # Transfrom printing coordinates to uArm coordinates, same ref point.
    xyarm_gcode = transform.coordinateTransfer(x_gcode, y_gcode, a_gcode, b_gcode, r_stage).T
    zarm_gcode = np.copy(z_gcode)  # z position, do no transform z coordinates



    # Start here-------

    swift.flush_cmd(wait_stop=True)
    if c == 0:
        swift.set_position(xyarm_gcode[0, 0], xyarm_gcode[0, 1], 10, speed=3000, timeout=20)
    else: 
        swift.set_position(xyarm_gcode[0, 0], xyarm_gcode[0, 1], Z0-15, speed=3000, timeout=20)
    time.sleep(0.2)
    swift.set_position(xyarm_gcode[0, 0], xyarm_gcode[0, 1], zarm_gcode[0], wait=True)

    if c == 0:
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
            ArduinoSerial.write(b'8') # Turn off printheads
            swift.set_position(xyarm_gcode[n, 0], xyarm_gcode[n, 1], zarm_gcode[n],
                               speed=spnp, wait=True)
        swift.flush_cmd()
        print(xyarm_gcode[n, 0],xyarm_gcode[n, 1],zarm_gcode[n])
    swift.set_position(xyarm_gcode[n, 0], xyarm_gcode[n, 1], Z0-15, speed=3000, timeout=20)
    time.sleep(0.3)
    ArduinoSerial.write(b'8') # Turn off all printheads at the end
    if i==0:
        ArduinoSerial.write(b'2') 
        time.sleep(0.4)
        ArduinoSerial.write(b'8') 

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