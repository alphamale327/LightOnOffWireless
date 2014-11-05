import serial
from xbee import XBee

PORT='/dev/ttyUSB0'
BAUD_RATE=57600
ser = serial.Serial(PORT, BAUD_RATE)
xbee=XBee(ser)
ser.write('1')
ser.close()
