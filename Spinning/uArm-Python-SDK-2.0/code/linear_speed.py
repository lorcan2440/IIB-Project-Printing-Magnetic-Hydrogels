# -*- coding: utf-8 -*-
"""
Created on Wed Jul 13 17:51:19 2022

@author: printer
"""
import os
import sys
import serial 
import time

ArduinoSerial = serial.Serial('COM4',2400) #COM3 is the port of syringe pump
time.sleep(2)

ArduinoSerial.write(b'3')
time.sleep(0.1)
ArduinoSerial.write(b'8')