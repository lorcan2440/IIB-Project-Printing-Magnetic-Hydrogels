import os
import sys
import serial 
import time
import numpy as np
import transformz
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI

# cd C:\Users\Biointerface\Documents\uArmPython\examples\Iek

# Import Arduino
ArduinoSerial = serial.Serial('COM3',2400)
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

def my_range(start, end, step):
    while start >= end:
        yield start
        start = start-step
    
# Setting

# Circle coordinates
Turn = np.linspace(0,2.7*2*np.pi, 40)[:-1]   
R = 0.09402*Turn**2-1.042*Turn-0.002899*Turn**3+5.745
x_spi = R * np.cos(Turn)
y_spi = R * np.sin(Turn)
z_spi = 0.122*Turn**2-0.388*Turn-0.00917*Turn**3+(2.26*10**(-4))*Turn**4-2.55
a_spi = 282.5-2  # mm
#282.5
b_spi = 1.5+4.5 # mm
#60 55
z0 = 60
spp = 15
#25
xyzarm_spi = transformz.coordinateTransfer(x_spi, y_spi, z_spi, a_spi, b_spi, z0).T
    
print('Cochlea coordinates: ')
for i in range(xyzarm_spi.shape[0]):
    print(xyzarm_spi[i])
print('')

# Print to std out for checking!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()


# Start here-------
print('\nMove to the first spiral position')
swift.flush_cmd(wait_stop=True)
swift.set_position(xyzarm_spi[0, 0]-8 , xyzarm_spi[0, 1], 10, speed=3000, timeout=20)
time.sleep(1)
#57.6
swift.set_position(xyzarm_spi[0, 0]-8 , xyzarm_spi[0, 1] , 62.6, wait=True)
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()
    
swift.set_buzzer(frequency=3000, duration=0.1)
ArduinoSerial.write(b'3')
time.sleep(3)
swift.set_position(xyzarm_spi[0, 0], xyzarm_spi[0, 1], 62.6, speed = 30, wait=True)

n = 0   
print('\nStart Cochlea printing')
swift.set_buzzer(frequency=3000, duration=0.1)
#spp+10*spp*n/45
for x, y, z in xyzarm_spi:
        swift.set_position(x, y, z,speed = spp+(n/40)*9*spp, wait=True)
        n =  n+1
        swift.flush_cmd(wait_stop=True)
                 
ArduinoSerial.write(b'5')        
swift.set_buzzer(frequency=3000, duration=0.1)
print('\nCircle printing finished')  

print('\nLowering nozzle to z = 10')
swift.set_position(z=10, speed=250, wait=True)
print('......')

print('\nReturn to starting position.(around X95 Y0 Z20)')
swift.set_position(x=200, y=0, z=10, speed=3000, wait=True)
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
