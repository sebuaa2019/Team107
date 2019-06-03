import serial
import re
ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
i = 0
while (i<=20):
    response = ser.readall().decode()
    result = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', response)
    if(result):
        print(result)
        break
    else:
        print('None: ' + str(i))
    i = i+1
