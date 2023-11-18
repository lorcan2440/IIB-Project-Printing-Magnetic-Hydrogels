# Import modules
import os
import sys
import serial 
import time
import numpy as np
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))
from uarm.wrapper import SwiftAPI

# cd C:\Users\Biointerface\Documents\uArmPython\examples\Iek

# Import my modules
#30000us
import transform 
import gcodemod

# Import Arduino
ArduinoSerial = serial.Serial('COM3',2400) #COM3 is the port of syringe pump
time.sleep(2)

# Print to std out for checking gcode!
isTerminate = input('Continue? Please type any key to continue [Y/n]: ')
if isTerminate == 'n':
    sys.exit()

print('pump extrusion')
ArduinoSerial.write(b'3') # Turn on printhead 3
time.sleep(3000)
ArduinoSerial.write(b'5') # Turn off printheads
ArduinoSerial.close()
print('done')