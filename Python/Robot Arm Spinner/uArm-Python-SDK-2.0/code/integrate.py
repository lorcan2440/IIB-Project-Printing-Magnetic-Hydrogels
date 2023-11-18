# Import modules
import os
import sys
import serial 
import time
import math
import keyboard
import fileinput
import coor_s #this should be the py file storing all the coordinates info
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI

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

duetSerial = serial.Serial(port='/dev/cu.usbmodem142401', baudrate=115200) 
ArduinoSerial = serial.Serial('/dev/cu.usbmodem142301',2400)
# Configure Duet
configFile = open('config.g', 'r')
configLines = configFile.readlines()

for line in configLines:
    print(line)

for line in configLines:
    duetSerial.write(str.encode(line + '\r\n'))  
# Arduino extrusion speed set
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

# the branch printing function
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


# the coor rewriting function   
def update_coor(file_path, variable_name, new_value):
    # Read the content of the file and update the variable
    with fileinput.FileInput(file_path, inplace=True) as file:
        for line in file:
            if line.startswith(variable_name):
                line = f'{variable_name} = {new_value}\n'
            print(line, end='')

    print('coordinates updated successfully!')
# function for adjusting the coorodinates
def coor_adjust(a, name, path):#here a is the coorarray, name is the str version like 'a', path is the path of coor_store
    print("use wasd to control xy position, ef for Z position and q to quit")
    stepsize=float(input('type stepsize you want'))
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
            update_coor(path,name,a)
            break
# print the fibers first
path_of_coor_s=''
t_s=10800#degrees per minute
spp1 = 20 # printing speed
n=3#cycles of moving during fiber printing
s1=0.04*spp1+0.09
a=coor_s.a#pos where the fiber printing strats
b=coor_s.b#pos where the fiber printing ends
d1=math.sqrt(((a[0]-b[0])**2+(a[1]-b[1])**2+(a[2]-b[2])**2))
t1=n*d1/s1
z1=t1*t_s/60

# print the fibers
duetSerial.write(str.encode('g1 h2 z90 f10800 \r\n'))

swift.set_position(a[0], a[1],10, wait=True)
swift.set_position(a[0], a[1],a[2], wait=True)
coor_adjust(a, 'a', path_of_coor_s)
    
swift.set_position(b[0], b[1],b[2], wait=True)
coor_adjust(b, 'b', path_of_coor_s)

# start printing fibers
i=1
swift.set_position(a[0], a[1],a[2], wait=True)
duetSerial.write(str.encode('g1 h2 z'+str(z1)+' f'+str(t_s)+' \r\n'))
ArduinoSerial.write(b'2')
while i<=n:
    swift.set_position(a[0], a[1],a[2], speed=spp1,wait=True)
    swift.set_position(b[0], b[1],b[2], speed=spp1,wait=True)
    i+=1
ArduinoSerial.write(b'5')
duetSerial.write(str.encode('g1 h2 z'+str(-z1%360)+' f10800 \r\n'))#tune the frame position back to horrizontal

# Channel printing
c=coor_s.c
d=coor_s.d
swift.set_position(c[0], c[1],10, wait=True)
swift.set_position(c[0], c[1],c[2], wait=True)
coor_adjust(c, 'c', path_of_coor_s)

swift.set_position(d[0], d[1],d[2], wait=True)
coor_adjust(d, 'd', path_of_coor_s)

 #frame length between in/outlets
l=math.sqrt(((c[0]-d[0])**2+(c[1]-d[1])**2+(c[2]-d[2])**2))
el= 1 #length of eachn part of the channel
interval= (l/2-2.5*el)/2
h=1 #height between different levels of branches
h_1=0.7
spp=16
q=1.5
o=1
v=1.9
z=d[2]
s_pos_1=[d[0]+q,d[1]+v,z]
s_pos_2=[d[0]+q,d[1]-v,z]    
swift.set_buzzer(frequency=1500, duration=0.1)
print('type s if continue')
ArduinoSerial.write(b'3')
while True:
    if keyboard.read_key()==('s'):
        break
time.sleep(2)
print('\nPrinting Pattern...')
swift.set_position(d[0]+o, d[1], z,speed=spp, wait=True)
swift.set_position(s_pos_1[0], s_pos_1[1], z,speed=spp, wait=True)
branch_print(s_pos_1,l,el,interval,h,h_1,spp)  

swift.set_position(c[0], c[1], z-10,speed=3000, wait=True)
ArduinoSerial.write(b'3')
swift.set_position(c[0]+o, c[1], z,speed=3000, wait=True)
swift.set_position(s_pos_2[0], s_pos_2[1], z,speed=spp, wait=True)
branch_print(s_pos_2,l,el,interval,h,h_1,spp)   
ArduinoSerial.write(b'5')
swift.set_buzzer(frequency=3000, duration=0.1)

swift.set_position(z=40, speed=3000, wait=True)

# dip in gel
e=coor_s.e
swift.set_position(e[0], e[1],e[2], wait=True)
coor_adjust(e, 'e', path_of_coor_s) 
swift.set_position(e[0], e[1],e[2]+10, wait=True)
duetSerial.write(str.encode('g1 h2 z180 f10800 \r\n'))
time.sleep(1.5)
swift.set_position(e[0], e[1],e[2], wait=True)
swift.set_position(e[0], e[1],e[2]+10, wait=True)
duetSerial.write(str.encode('g1 h2 z180 f10800 \r\n'))
time.sleep(1.5)

#UV chamber
f=coor_s.f
swift.set_position(f[0], f[1],f[2], wait=True)
coor_adjust(f, 'f', path_of_coor_s) 

# go to the front
g=coor_s.g
swift.set_position(g[0], g[1],g[2], wait=True)
coor_adjust(g, 'g', path_of_coor_s) 

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

