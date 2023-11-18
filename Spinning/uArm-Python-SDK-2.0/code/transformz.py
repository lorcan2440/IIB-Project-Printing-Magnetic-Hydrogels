#!/usr/bin/env python
import numpy as np

def coordinateTransfer(x, y, z, a, b, z0, r=33):
    # Transform from printing coordinates to robotic arm's coordinates
    # 
    # All unit is in mm!
    #
    # Inputs
    # x: printing x-coordinate (from the 'mid-point')
    # y: printing y-coordinate (from the 'mid-point')
    # a: mid-point x-coordinate
    # b: mid-point y-coordinate
    # 
    # Note: mid-point (a,b) is in terms of 'robotic arm direction'
    #       printing coordinate (x,y) is 'real x,y direction'
    # printhead 2 (a,b) = (282,76)
    # printhead 3 (a,b) = (282.5,2)
    # printhead 4 (a,b) = (280,-74)
    x = np.asarray(x, dtype=np.float)
    y = np.asarray(y, dtype=np.float)
    z0 = np.asarray(z0, dtype=np.float)
    xroot = a + y
    yroot = b - x
    theta = np.arctan2(yroot, xroot)
    xarm = xroot - r * np.cos(theta)
    yarm = yroot - r * np.sin(theta)
    zarm = z0 - z
    return np.around([xarm, yarm, zarm], decimals=1)
    
#  example
x = [21,-21]  # mm
y = [0,0]
z = [0,0]
a = 281.5  # mm
b = 75# mm
z0 = 58.0
xyarm = coordinateTransfer(x, y, z, a, b, z0)
for i in range(xyarm.shape[1]):
    print(xyarm[:, i])