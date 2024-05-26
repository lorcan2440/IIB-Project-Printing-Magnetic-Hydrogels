# Import modules
import os
import sys
import time
import threading

# import the robot arm library
sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))
from uarm.wrapper import SwiftAPI

# editable parameters
DEFAULT_POSITION = [250, 0, 115]

# connect to the robot
swift = SwiftAPI(filters={"hwid": "USB VID:PID=2341:0042"})
swift.waiting_ready(timeout=3)
device_info = swift.get_device_info()
print(device_info)
firmware_version = device_info["firmware_version"]
if firmware_version and not firmware_version.startswith(("0.", "1.", "2.", "3.")):
    swift.set_speed_factor(0.0005)
swift.set_mode(0)

# move to default position
print('Moving to default position.')
swift.set_position(*DEFAULT_POSITION, speed=1000, wait=True)

while True:
    pos = swift.get_position(wait=True, timeout=None, callback=None)
    print(f'Current position: x = {pos[0]}, y = {pos[1]}, z = {pos[2]}.')
    print('Enter movement command e.g. "x 50" to move 50 mm in the x-direction.')
    entry = input()
    try:
        axis, distance = entry.split()
        distance = float(distance)
        if axis == 'x':
            swift.set_position(pos[0] + distance, pos[1], pos[2], speed=1000, wait=True)
        elif axis == 'y':
            swift.set_position(pos[0], pos[1] + distance, pos[2], speed=1000, wait=True)
        elif axis == 'z':
            swift.set_position(pos[0], pos[1], pos[2] + distance, speed=1000, wait=True)
        else:
            print('Invalid axis. Please enter "x", "y" or "z" followed by a number.')
            continue
    except (ValueError, TypeError):
        if entry == '':
            break
        else:
            print('Invalid entry. Please enter an axis followed by a number.')
            continue
