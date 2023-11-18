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
ArduinoSerial = serial.Serial('COM5',2400) #COM5 is the port of syringe pump
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
spp = 15  # Printing speed
spnp = 1000  # Not printing speed 
Z0 = 52.7 # starting z position

for num, offset_i in enumerate([[11, 0, Z0], [5, 0, Z0], [-1, 0, Z0], [-7, 0, Z0]]):
    printhead = 5
    stage = 3 #1 Small, 2 Large, 3 square box


    bigCoor = gcodemod.read(r"C:\Users\49250\Documents\uArm-Python-SDK-2.0\code\box_221.8.txt", offset_i) # Import gcode

    x_gcode = bigCoor[:, 0] # Import x coord from gcode file
    y_gcode = bigCoor[:, 1] # Import y coord from gcode file
    z_gcode = bigCoor[:, 2] # Import z coord from gcode file
    e_gcode = bigCoor[:, 3]  # Import extrusion information from gcode file 


    # X-Y coordinates transformation
    ab = [[180.5,76], [254,-4], [280,-74], [254, 4.2]] #Calibrated printhead 2,3,4 a,b coordinates
    stage_mega_r = [33, 44.5, 38]
    a_gcode = ab[printhead-2][0] # x coord of the printhead from uArm base, mm 
    b_gcode = ab[printhead-2][1] # y coord of the printhead from uArm base, mm
    r_stage = stage_mega_r[stage-1]

    # Transfrom printing coordinates to uArm coordinates, same ref point.
    xyarm_gcode = transform.coordinateTransfer(x_gcode, y_gcode, a_gcode, b_gcode, r_stage).T
    zarm_gcode = np.copy(z_gcode)  # z position, do no transform z coordinates

    print('\nMove to the Z position')
    swift.flush_cmd(wait_stop=True)
    swift.set_position(xyarm_gcode[0, 0], xyarm_gcode[0, 1], 10, speed=3000, timeout=20)
    time.sleep(1)
    swift.set_position(xyarm_gcode[0, 0], xyarm_gcode[0, 1], zarm_gcode[0], wait=True)
    # this is to check the x,y position, so the Z is a bit lower just to ensure no extra injection of cells
    stepsize=0.1
    print("use wasd to control xy position, ef for Z position and t to terminate")
    z_d=0
    while True:
        if keyboard.read_key()==('e'):
            z_d=z_d+0.1
        if keyboard.read_key()==('f'):
            z_d=z_d-0.1
        swift.set_position(xyarm_gcode[0, 0], xyarm_gcode[0, 1],zarm_gcode[0]+z_d, wait=True)
        if keyboard.read_key()==('q'):
            break
    

    
#offset = [0, 0, Z0] # Setting as [0,0,Z0] means printing at the central point (a_gcode,b_gcde) of the stage at Z0
    
    # set arduino
    print('Gcode coordinates: ')
    for i in range(xyarm_gcode.shape[0]):
        print(np.append(xyarm_gcode[i], zarm_gcode[i]+z_d))
    print('')

# Print to std out for checking Z0!
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
    
    print('\nStart gcode printing')
    swift.set_buzzer(frequency=3000, duration=0.1)
    ArduinoSerial.write(b'3') # Turn on printhead 3
    time.sleep(1.5)
    for n, etem in enumerate(e_gcode):
        if etem == 1: # printing
            ArduinoSerial.write(b'3') # Turn on printhead 3
            swift.set_position(xyarm_gcode[n, 0], xyarm_gcode[n, 1], zarm_gcode[n]+z_d,
                    speed=spp, wait=True)
        elif etem == 0: # stop printing
            ArduinoSerial.write(b'5') # Turn off printheads
            swift.set_position(xyarm_gcode[n, 0], xyarm_gcode[n, 1], zarm_gcode[n]+z_d,
                    speed=spnp, wait=True)
        swift.flush_cmd()
        print(xyarm_gcode[n, 0],xyarm_gcode[n, 1],zarm_gcode[n]+z_d)

    ArduinoSerial.write(b'6') 
    time.sleep(3.5)   
    ArduinoSerial.write(b'5') # Turn off all printheads at the end
    swift.set_buzzer(frequency=3000, duration=0.1)
    print('\nGcode printing finished')  

    print('\nLowering nozzle to z = 10')
    swift.set_position(z=10, speed=3000, wait=True)
    print('......')
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