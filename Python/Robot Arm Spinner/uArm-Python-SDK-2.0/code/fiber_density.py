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
MOTION_RANGE = 8
PRINTING_SPEED = 30
PRINTING_AXIS = 'y'  # x: forwards and backwards, y: left and right, z: up and down
PRINT_TIME = 99999  # move the robot arm for 120 seconds

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

# allow manual setting of the z-axis position (height above reference point in mm)
print('Minimum allowed z = -25 mm. Maximum allowed z = 160 mm.')
while True:
    pos = swift.get_position(wait=True, timeout=None, callback=None)
    print(f'Current (x, y, z) position (mm): {pos}.')
    entry = input("Adjust Z-axis position by how much (mm)? Press enter to continue. ")
    if entry == '':
        break
    else:
        try:
            new_z = pos[2] + float(entry)
            swift.set_position(pos[0], pos[1], new_z, speed=1000, wait=True)
        except (ValueError, TypeError):
            print("Invalid entry. Please enter a number to change the z-coordinate by in mm.")
            continue

# confirm ready to start print
pos = swift.get_position(wait=True, timeout=None, callback=None)
entry = input(f'Current z-axis position: {pos[2]}. Ready to start fibre printing, press "y" to go or anything else to exit. ')
if entry.lower() != 'y':
    print("Ending program.")
    exit(code=0)


def move_robot():
    i = 0
    t_start = time.time()
    while time.time() - t_start < PRINT_TIME:
        print(f'Starting pass {i+1}.')
        # move to other side
        if PRINTING_AXIS == 'x':
            swift.set_position(pos[0] - MOTION_RANGE, pos[1], pos[2], speed=PRINTING_SPEED, wait=True)
        elif PRINTING_AXIS == 'y':
            swift.set_position(pos[0], pos[1] - MOTION_RANGE, pos[2], speed=PRINTING_SPEED, wait=True)
        # move back
        swift.set_position(pos[0], pos[1], pos[2], speed=PRINTING_SPEED, wait=True)
        i += 1


robot_thread = threading.Thread(target=move_robot, daemon=True)
robot_thread.start()
robot_thread.join(timeout=PRINT_TIME)
print(f'Fibre printing complete after {PRINT_TIME} seconds. Moving to default position.')
swift.set_position(*DEFAULT_POSITION, speed=1000, wait=True)
