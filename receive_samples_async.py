#! /usr/bin/python

"""
receive_samples_async.py

By Paul Malmsten, 2010
pmalmsten@gmail.com

This example reads the serial port and asynchronously processes IO data
received from a remote XBee.
"""

from xbee import XBee
import time
import serial
import update

#PORT = '/dev/tty.usbserial-FTFOHO9D'
PORT = '/dev/ttyUSB0'
BAUD_RATE = 57600

# Open serial port
ser = serial.Serial(PORT, BAUD_RATE)

def message_received(data):
	print data
	try :
		datadict=data
		
		#get field containing batterylevel, temperature and carcount
		values = datadict["rf_data"]

		#remove dangerous characters
		values = values.replace("\r", "")
		values = values.replace("\n", "")

		#grab id, it's given as a raw binary number
		idstr = datadict["source_addr"]
		id = ord(idstr[0]) * 256 + ord(idstr[1])

		valuesplit = values.split()
		#convert batterylevel, temperature and carcount into numbers, batterylevel in percentage
		carcount = int(valuesplit[0])
		battery = int((float(valuesplit[1])-2.7)/(4.23-2.7)*100)
		temperature = float(valuesplit[2])

		#submit everything
		update.doPost(id, carcount, battery)

	except Exception as e:
		#the last steps will fail for messages such as on calibration, we need to catch this
		pass
    

# Create API object, which spawns a new thread
xbee = XBee(ser, callback=message_received)

# Do other stuff in the main thread
while True:
    try:
        time.sleep(.1)
    except KeyboardInterrupt:
        break

# halt() must be called before closing the serial
# port in order to ensure proper thread shutdown
xbee.halt()
ser.close()
