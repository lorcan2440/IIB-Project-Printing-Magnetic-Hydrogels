# -*- coding: utf-8 -*-
"""
Created on Wed Apr 20 19:03:33 2022

@author: printer
"""

import os
import sys
import serial 
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
ArduinoSerial = serial.Serial('COM4',2400) #COM3 is the port of syringe pump
time.sleep(2)
# Import syringe Pump Arduino

while True:
    n=1
    while n<=7:
        ArduinoSerial.write(b'2')
        time.sleep(190)
        ArduinoSerial.write(b'5')
        time.sleep(40)
        n=n+1
    while n<=14:
        ArduinoSerial.write(b'1')
        time.sleep(190)
        ArduinoSerial.write(b'5')
        time.sleep(40)
        n=n+1
