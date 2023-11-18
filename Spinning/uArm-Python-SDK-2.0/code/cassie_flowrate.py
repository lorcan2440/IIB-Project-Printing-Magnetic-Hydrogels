# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 21:26:50 2022

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

isTerminate = input('Turn on pump? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    ArduinoSerial.write(b'5') # Turn off stepper motors
    sys.exit()

    
 #start the pumps
ArduinoSerial.write(b'1')
time.sleep(900) #run for 15 mins
#reverse drn
ArduinoSerial.write(b'2')
time.sleep(900) #run for 15 mins
ArduinoSerial.write(b'5') #stop the pump
sys.exit()