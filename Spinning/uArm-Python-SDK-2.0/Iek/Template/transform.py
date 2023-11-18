#!/usr/bin/env python
import numpy as np

def coordinateTransfer(x, y, a, b, r=33):
    # Transform printing coordinates to robotic arm's coordinates
    # Generate coordinates with respect to the uArm Base coordinates
    # All unit is in mm!
    #
    # Inputs
    # x: printing x-coordinate (from the 'mid-point')
    # y: printing y-coordinate (from the 'mid-point')
    # a: mid-point x-coordinate from uArm base
    # b: mid-point y-coordinate from uArm base
    # r: distance between the central point of the stage and uArm detector
    
    # Note: mid-point (a,b) is in 'robotic arm direction'
    #       printing coordinate (x,y) is in 'real x,y direction'
    # printhead 2 (a,b) = (282,76)
    # printhead 3 (a,b) = (282.5,2)
    # printhead 4 (a,b) = (280,-74)
    # Return a set of input coordinates for robotic arm 
    x = np.asarray(x, dtype=np.float)
    y = np.asarray(y, dtype=np.float)
    xroot = a + y
    yroot = b - x
    theta = np.arctan2(yroot, xroot)
    xarm = xroot - r * np.cos(theta)
    yarm = yroot - r * np.sin(theta)
    return np.around([xarm, yarm], decimals=1)
    
#  example
if __name__ == '__main__':
    x = [0]  # mm
    y = [0]  # mm
    a = 282.5  # mm
    b = 1.5 # mm
    xyarm = coordinateTransfer(x, y, a, b)
    for i in range(xyarm.shape[1]):
        print(xyarm[:, i])
    print('...')
    print(xyarm.T[-1])
    print(xyarm.T[-1, 0])