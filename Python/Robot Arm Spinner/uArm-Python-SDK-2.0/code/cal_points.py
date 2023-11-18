
# Import modules
import os
import sys
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
path_of_coor_s='/Users/yaqi/Desktop/uArm-Python-SDK-2.0/code/coor_s.py'
k=swift.get_position()
print(k)
coor_adjust(k, 'a', path_of_coor_s)#only 'a' needs to be changed