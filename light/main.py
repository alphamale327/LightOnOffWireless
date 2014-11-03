#Light ON OFF
from serialinterface import serialThread
from collections import deque
import serial
from xbee import XBee
import datetime
import time
import os.path

PORT='/dev/ttyUSB0'
BAUD_RATE=57600

data_queue = deque([])
command_queue = deque([])
serialMonitor = serialThread(1, PORT, BAUD_RATE,1, data_queue, command_queue)
serialMonitor.start()

ser = serial.Serial(PORT, BAUD_RATE)

# ZB XBee here. If you have Series 1 XBee, try XBee(ser) instead
xbee=XBee(ser)

#MAC, number written on the back of the XBee module
# HUB = my hub
# EP1 = my endpoint
device={
        "HUB":'\x00\x13\xa2\x00\x40\xa7\x9b\xad',
        "EP1":'\x00\x13\xa2\x00\x40\xb3\x65\x5c'
}

logfile = datetime.datetime.now().strftime('%b_%d_%Y')
if not os.path.isfile('/var/www/logFiles/%s.txt' %logfile):
    f = open('/var/www/logFiles/%s.txt' %logfile, 'w')
    f.close

def writeLog(string):
    global logfile
    daynow = datetime.datetime.now().strftime('%b_%d_%Y')
    timestamp = datetime.datetime.now().strftime('%B%d_%Y %I:%M:%S')
    if daynow == logfile:
        f = open('/var/www/logFiles/%s.txt' %logfile, 'a')
    else:
        logfile = datetime.datetime.now().strftime('%b_%d_%Y')
        f = open('/var/www/logFiles/%s.txt' %logfile, 'w')
    f.write('%s     %s' %(timestamp, string))
    f.close

writeLog('HUB started\n')    
while True:
    time.sleep(1)
    # Check Data Queue
    if len(data_queue) > 0:
        data = data_queue.popleft()

        if data[0] == 'command_executed':
            print 'Command executed: ' + data[1]
            writeLog('Command executed: ' + data[1] + '\n')
    
    command_file = open("/var/www/web/command.txt", "r+")
    command = command_file.read()
    if command != '':
        print 'Command received: ' + command 
        command_queue.append(command)
        
        # Motion Sensing Disable
        if command == '1': 
            print 'Light ON / OFF Excute'
            writeLog('Light ON / OFF Excuted\n')
            # xbee.remote_at(dest_addr_long=device["EP1"],command='D0',parameter='\x05')
            # time.sleep(1)		
            # xbee.remote_at(dest_addr_long=device["EP1"],command='D0',parameter='\x04')
        # Enable Motion Detecting
        command_file.seek(0)
        command_file.truncate()
    command_file.close()