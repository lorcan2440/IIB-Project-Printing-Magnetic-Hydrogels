# Import modules
import os
import sys
import serial 
import time
import numpy as np
import transform
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI
import keyboard

ArduinoSerial = serial.Serial('COM3',2400) #COM5 is the port for arduino 
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
def convert_to_arduino(number):
    while number > 30000 or number <= 0:
        number = int(input('input the delaytime you want to set, maximum 30000, the larger the delaytime is the slower the pump will be, dont set it too small!'))
    else:
        length = len(str(number))
    
    if length == 1: #send first charater to the Arduino, let it know how many numbers it needs to wait before convert numbers in buffer into delaytime)
        ArduinoSerial.write(b'1')
    if length == 2:
        ArduinoSerial.write(b'2')
    if length == 3:
        ArduinoSerial.write(b'3')
    if length == 4:
        ArduinoSerial.write(b'4')
    if length == 5:
        ArduinoSerial.write(b'5')
    
    for i in str(number):#send numbers in the delaytime individually
        print(i)
        if int(i) == 0:
            ArduinoSerial.write(b'0')
        if int(i) == 1:
            ArduinoSerial.write(b'1')
        if int(i) == 2:
            ArduinoSerial.write(b'2')
        if int(i) == 3:
            ArduinoSerial.write(b'3')
        if int(i) == 4:
            ArduinoSerial.wrie(b'4')
        if int(i) == 5:
            ArduinoSerial.write(b'5')
        if int(i) == 6:
            ArduinoSerial.write(b'6')
        if int(i) == 7:
            ArduinoSerial.write(b'7')
        if int(i) == 8:
            ArduinoSerial.write(b'8')
        if int(i) == 9:
            ArduinoSerial.write(b'9')  
    print('Delaytime sent to Arduino!')
convert_to_arduino(30000)  
# Setting equations
a_org = -5
n = 2
L = 10
w = 30
b_org = -5
x_coor_mega = [a_org+w, a_org]
y_coor_mega = [b_org, b_org]

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

for num in range(n):
    if num == 0:
        a = a_org
    if num > 0:
        a = a + w/n
    b = b_org
        
    x_coord = [a, a, a+w/(2*n), a+w/(2*n), a+w/n]
    y_coord = [b+L, b, b, b+L, b+L]
    
    for i, j in zip(x_coord, y_coord):
        x_coor_mega.append(i)
        y_coor_mega.append(j)
x_coor_mega.append(a_org+w)
x_coor_mega.append(a_org+w)
x_coor_mega.append(a_org)
y_coor_mega.append(b_org+L)
y_coor_mega.append(b_org)
y_coor_mega.append(b_org)   

# Printing parameters
s = 0.3 # Layer height 0.3
z = 45 # Starting z position
spp = 40 # printing speed
L1 = 0.3 # Thickness of the construct, mm
  
a_cir = 282.5  # x coord of the printhead from uArm base, mm
b_cir = 1.5 # y coord of the printhead from uArm base, mm
a=[a_cir-45,b_cir,z]
swift.set_position(a[0], a[1],a[2], wait=True)

stepsize=float(input(' what is the stepsize you want?'))
print("use wasd to control xy position, ef for Z position and q to quit")
while True:
    if keyboard.read_key()==('a'):
        a[0]=a[0]+stepsize
    if keyboard.read_key()==('d'):
        a[0]=a[0]-stepsize
    if keyboard.read_key()==('s'):
        a[1]=a[1]+stepsize
    if keyboard.read_key()==('w'):
        a[1]=a[1]-stepsize
    if keyboard.read_key()==('e'):
        a[2]=a[2]+stepsize
    if keyboard.read_key()==('f'):
        a[2]=a[2]-stepsize
    swift.set_position(a[0], a[1],a[2], wait=True)
    if keyboard.read_key()==('q'):
        break
a_cir=a[0]+45
b_cir=a[1]
z=a[2]
xyarm_cir = transform.coordinateTransfer(x_coor_mega, y_coor_mega, a_cir, b_cir,45).T     
print('Circle coordinates: ')
for i in range(xyarm_cir.shape[0]):
    print(xyarm_cir[i])
print('')

# Print to std out for checking!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()



# Start here-------
print('\nMove to the first circle position')
swift.flush_cmd(wait_stop=True)
swift.set_position(xyarm_cir[0, 0], xyarm_cir[0, 1], 10, speed=3000, timeout=20)
time.sleep(1)
swift.set_position(xyarm_cir[0, 0], xyarm_cir[0, 1], z, wait=True)


# Print to std out for checking!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()

    
print('\nStart Circle printing')
swift.set_buzzer(frequency=3000, duration=0.1)
ArduinoSerial.write(b'3')
time.sleep(5)

print('\nPrinting a cirlce at %.2f' % z)
for x, y in xyarm_cir:
    swift.set_position(x, y, z,speed=spp, wait=True)
swift.flush_cmd(wait_stop=True)  

ArduinoSerial.write(b'5')   
 # Turn off printheads       
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