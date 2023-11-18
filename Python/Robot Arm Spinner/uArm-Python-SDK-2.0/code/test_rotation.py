# Import modules
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI
import serial
import time

# cd C:\Users\Biointerface\Documents\uArmPython\examples\Template

ArduinoSerial = serial.Serial('/dev/cu.usbmodem144401',2400) #COM3 is the port of syringe pump
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

a = swift.get_position(wait=True, timeout=None, callback=None)
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
ArduinoSerial.write(b'1')
print("adjust z pos")
while True:
    a[2]=a[2]+float(input())
    swift.set_position(a[0], a[1],a[2], wait=True)
    isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
    if isTerminate == 'n':
        break

i=1
spp = 15 # printing speed
k=0
while k<3: 
    k+=1
    swift.set_position(a[0]+3, a[1], a[2],speed=spp, wait=True)
    swift.set_position(a[0]-3, a[1], a[2],speed=spp, wait=True)
    
ArduinoSerial.write(b'2')
while True:
    isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
    ArduinoSerial.write(b'1')
    k=0
    while k<3: 
        k+=1
        swift.set_position(a[0]+5, a[1], a[2],speed=spp, wait=True)
        swift.set_position(a[0]-5, a[1], a[2],speed=spp, wait=True)
    ArduinoSerial.write(b'2')
    



ArduinoSerial.close()

