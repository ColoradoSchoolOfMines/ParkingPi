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
		#convert batterylevel, temperature and carcount into numbers, batterylevel in percentage and grab window of points associated to car detection
		carcount = int(valuesplit[0])
		battery = int((float(valuesplit[1])-2.7)/(4.23-2.7)*100)
		temperature = float(valuesplit[2])
		#depending on how we send them from the sensor, this should grab all the points in the window, even if we don't know its length
		pointWindow = valuesplit[3:]#should grab the rest of the values and store them as the window 

		window = []
		for point in pointWindow:
			values = point.split(',')
			x = int(values[0])
			y = int(values[1])
			z = int(values[2])
			window.append("%s %s %s" %(x, y, z))

		#submit everything
		update.doPost(id, carcount, battery, temperature, window)

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
