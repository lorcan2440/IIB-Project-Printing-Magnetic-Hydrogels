import os
import sys
import serial 
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI
import keyboard 


#import Arduino
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

def branch_print(s_pos,l,el,interval,h,h_1,spp):
    x_cor=[s_pos[0]]
    y_cor=[s_pos[1]]

#define dots of the first printing path (cedf are 4 critical points)
    x_temp=[s_pos[0]+el, s_pos[0]+el+interval, s_pos[0]+2*el+interval, s_pos[0]+2*el+2*interval]
    y_temp=[s_pos[1],s_pos[1]-h, s_pos[1]-h, s_pos[1]-h-h_1]
    x_cor+=x_temp
    y_cor+=y_temp
    c=[s_pos[0]+el, s_pos[1]]
    d=[s_pos[0]+el+interval,s_pos[1]-h]
    e=[s_pos[0]+2*el+interval,s_pos[1]-h]
    f=[s_pos[0]+2*el+2*interval,s_pos[1]-h-h_1]

    x_temp=[f[0]+el,e[0]+el+2*interval,e[0]+2*el+2*interval, e[0]+2*el+3*interval, a[0]]
    y_temp=[f[1], e[1], d[1], c[1], a[1]]

    x_cor+=x_temp
    y_cor+=y_temp

    z=s_pos[2]

#define dots of the first branch 
    K=x_cor
    M=y_cor
    x_cor_2=[K[6],K[5],K[4],K[3]]
    y_cor_2=[M[6],M[5]+2*h_1, M[4]+2*h_1, M[3]]

#define the dots of the second
    x_cor_3=x_cor[1:len(x_cor)-1]
    y_cor_3=[M[1], M[2]+2*h, M[3]+2*h, M[4]+2*h+2*h_1, M[5]+2*h+2*h_1, M[6]+2*h, M[7]+2*h, M[8]]

#define dots of the second branch 
    K=x_cor_3
    M=y_cor_3
    x_cor_4=[K[5],K[4],K[3],K[2]]
    y_cor_4=[M[5],M[4]-2*h_1, M[3]-2*h_1, M[2]]
   
# start printing
    i=0
    while i<=len(x_cor)-1:#print the first channel
        swift.set_position(x_cor[i], y_cor[i], z,speed=spp, wait=True)
        swift.flush_cmd(wait_stop=True)
        i+=1
    ArduinoSerial.write(b'5') 
    swift.set_position(z=b[2]-2, speed=500, wait=True)

    ArduinoSerial.write(b'3')
    swift.set_position(x_cor_2[0],y_cor_2[0],z, speed=500, wait=True)
    i=1
    while i<=len(x_cor_2)-1:#print the first branch
        swift.set_position(x_cor_2[i], y_cor_2[i], z,speed=spp, wait=True)
        swift.flush_cmd(wait_stop=True)
        i+=1
    ArduinoSerial.write(b'5') 
    swift.set_position(z=b[2]-2, speed=500, wait=True)

    ArduinoSerial.write(b'3')
    swift.set_position(x_cor_3[0],y_cor_3[0],z, speed=500, wait=True)
    i=1
    while i<=len(x_cor_3)-1:#print the second channel
        swift.set_position(x_cor_3[i], y_cor_3[i], z,speed=spp, wait=True)
        swift.flush_cmd(wait_stop=True)
        i+=1
    ArduinoSerial.write(b'5') 
    swift.set_position(z=b[2]-2, speed=3000, wait=True)

    ArduinoSerial.write(b'3')
    swift.set_position(x_cor_4[0],y_cor_4[0],z, speed=3000, wait=True)
    i=1
    while i<=len(x_cor_4)-1:#print the second branch
        swift.set_position(x_cor_4[i], y_cor_4[i], z,speed=spp, wait=True)
        swift.flush_cmd(wait_stop=True)
        i+=1
    ArduinoSerial.write(b'5') # Turn off printheads   


def my_range(start, end, step):
    while start >= end:
        yield start
        start = start-step
#set parameters

z=60
l=7.7
swift.set_position(258, -7,10, wait=True)
swift.set_position(258, -7,z, wait=True)
a = swift.get_position(wait=True, timeout=None, callback=None)
delaytime = 30000 
convert_to_arduino(delaytime) # Send delaytime to Arduino
# Print to std out for checking!

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
print(a)
z=a[2]
swift.set_position(a[0]-l, a[1],10, wait=True)
swift.set_position(a[0]-l, a[1],z, wait=True)
b = swift.get_position(wait=True, timeout=None, callback=None)

stepsize=float(input('Hi Adash, what is the stepsize you want?'))
print("use wasd to control xy position, ef for Z position and q to quit")
while True:
    if keyboard.read_key()==('a'):
        b[0]=b[0]+stepsize
    if keyboard.read_key()==('d'):
        b[0]=b[0]-stepsize
    if keyboard.read_key()==('s'):
        b[1]=b[1]+stepsize
    if keyboard.read_key()==('w'):
        b[1]=b[1]-stepsize
    if keyboard.read_key()==('e'):
        b[2]=b[2]+stepsize
    if keyboard.read_key()==('f'):
        b[2]=b[2]-stepsize
    swift.set_position(b[0], b[1],b[2], wait=True)
    if keyboard.read_key()==('q'):
        break
print(b)
 #frame length between in/outlets
zoom=3#set the zoom in ratio of the channel pattern to print larger
l=7*zoom
el= 1*zoom #length of eachn part of the channel
interval= (l/2-2.5*el)/2
h=1*zoom #height between different levels of branches
h_1=0.7*zoom
spp=16
q=1.5*zoom
o=1*zoom
v=1.9*zoom
z=b[2]
s_pos_1=[b[0]+q,b[1]+v,z]
s_pos_2=[b[0]+q,b[1]-v,z]


swift.set_buzzer(frequency=1500, duration=0.1)
print('type s if continue')
ArduinoSerial.write(b'3')
while True:
    if keyboard.read_key()==('s'):
        break
time.sleep(2)
print('\nPrinting Pattern...')
#print the first big branch
swift.set_position(b[0]+o, b[1], z,speed=spp, wait=True)
swift.set_position(s_pos_1[0], s_pos_1[1], z,speed=spp, wait=True)
branch_print(s_pos_1,l,el,interval,h,h_1,spp)
#swift.set_position(a[0]-o, a[1]+v, z,speed=spp, wait=True)
#swift.set_position(a[0]-o, a[1], z,speed=spp, wait=True)
#swift.set_position(a[0], a[1], z,speed=spp, wait=True)

#print the second big branch
swift.set_position(a[0], a[1], 50,speed=3000, wait=True)
ArduinoSerial.write(b'3')
swift.set_position(b[0]+o, b[1], z,speed=3000, wait=True)
swift.set_position(s_pos_2[0], s_pos_2[1], z,speed=spp, wait=True)
branch_print(s_pos_2,l,el,interval,h,h_1,spp)
#swift.set_position(a[0]-o, a[1]-v, z,speed=spp, wait=True)
#swift.set_position(a[0]-o, a[1], z,speed=spp, wait=True)
#swift.set_position(a[0], a[1], z,speed=spp, wait=True)
ArduinoSerial.write(b'5')
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