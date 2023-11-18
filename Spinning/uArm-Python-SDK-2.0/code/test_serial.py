# Import modules
import os
import sys
import serial 
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '../../..'))


# cd C:\Users\Biointerface\Documents\uArmPython\examples\Template



# Import Arduino
ArduinoSerial = serial.Serial('COM5',2400) #COM5 is the port of syringe pump
time.sleep(2)
number=31000
while number>30000 or number <=0:
    number=int(input('input the delaytime you want to set, maximum 30000, the larger the delaytime is the slower the pump will be, dont set it too small!'))
else:
    length=len(str(number))

if length==1: #send first charater to the Arduino, let it know how many numbers it needs to wait before convert numbers in buffer into delaytime)
    ArduinoSerial.write(b'1')
if length==2:
    ArduinoSerial.write(b'2')
if length==3:
    ArduinoSerial.write(b'3')
if length==4:
    ArduinoSerial.write(b'4')
if length==5:
    ArduinoSerial.write(b'5')

for i in str(number):#send numbers in the delaytime individually
    print(i)
    if int(i)==0:
        ArduinoSerial.write(b'0')
    if int(i)==1:
        ArduinoSerial.write(b'1')
    if int(i)==2:
        ArduinoSerial.write(b'2')
    if int(i)==3:
        ArduinoSerial.write(b'3')
    if int(i)==4:
        ArduinoSerial.write(b'4')
    if int(i)==5:
        ArduinoSerial.write(b'5')
    if int(i)==6:
        ArduinoSerial.write(b'6')
    if int(i)==7:
        ArduinoSerial.write(b'7')
    if int(i)==8:
        ArduinoSerial.write(b'8')
    if int(i)==9:
        ArduinoSerial.write(b'9')

time.sleep (2)    # wait untill parseint function complete
ArduinoSerial.write(b'3') # turn on printhead 3

time.sleep(8)
ArduinoSerial.write(b'5') # turn off printhead 3
ArduinoSerial.close()

