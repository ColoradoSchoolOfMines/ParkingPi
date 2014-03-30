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
STORAGE = {} #stores the data until it gets its paired data

# Open serial port
ser = serial.Serial(PORT, BAUD_RATE)


def parseDataAndSend(id, dataStream):
	#get the < and > out of datastream
	dataStream = dataStream.replace("<", "")
	dataStream = dataStream.replace(">", "")

	valuesplit = dataStream.split()
	carcount = valuesplit[0]
	voltage = valuesplit[1]
	temperature = valuesplit[2]
	window = valuesplit[3:]
	update.doPost(id, carcount, voltage, temperature, window)


def message_received(data):
	print data
	try :
		datadict=data
		
		#get field containing voltagelevel, temperature and carcount
		values = datadict["rf_data"]

		#remove dangerous characters
		values = values.replace("\r", "")
		values = values.replace("\n", "")

		#grab id, it's given as a raw binary number
		idstr = datadict["source_addr"]
		#get the id, and make sure that there are 
		id = ord(idstr[0]) * 256 + ord(idstr[1])
		if id in STORAGE: #case where were still recieving data
			if values.find("[") != -1: #there is a segment to ignore
				None
			elif values.find(">") == -1: #not the end of data stream
				STORAGE[id] += values
			else:
				STORAGE[id] += values
				parseDataAndSend(id, STORAGE[id])
				del STORAGE[id]
		else: #new data recived for an id not in STORAGE
			STORAGE[id] = values
			
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

"""

def message_received(data):
	print data
	window = []
	tempStorage = {}
	carcount = None
	previousID = None
	while window == [] or carcount == None: #keep listening until you have the local count, volt, temp, and the window
		try :
			datadict=data
			
			#get field containing voltagelevel, temperature and carcount
			values = datadict["rf_data"]

			#remove dangerous characters
			values = values.replace("\r", "")
			values = values.replace("\n", "")

			#grab id, it's given as a raw binary number
			idstr = datadict["source_addr"]
			#get the id, and make sure that there are 
			if previousID == None:
				id = ord(idstr[0]) * 256 + ord(idstr[1])
				previousID = id
			else:
				if ord(idstr[0]) * 256 + ord(idstr[1]) != previousID:
					

			valuesplit = values.split()
			if valuesplit[0] != 'w': #if the first character isn't the identifier char, then were collecting the local count, voltage, and temperature
				carcount = int(valuesplit[0])
				voltage = float(valuesplit[1])
				temperature = float(valuesplit[2])
			else: #the data were getting is window data	
				for i in range(1, len(valuesplit)):
					window.append(float(valuesplit[i]))
					


		except Exception as e:
			#the last steps will fail for messages such as on calibration, we need to catch this
			pass
		
	#submit everything
	update.doPost(id, carcount, voltage, temperature, window)
"""
#		if id in STORAGE: #if the id is in STORAGE
#			if STORAGE[id] == None: #this is an extreme edge case, the id should never be added unless there was data before
#				if valuesplit[0] != 'w': #if the first character isn't the identifier char, then were collecting the local count, voltage, and temperature
#					point = DataStream()
#					point.carcount = int(valuesplit[0])
#					point.voltage = float(valuesplit[1])
#					point.temperature = float(valuesplit[2])
#					STORAGE[id] = point
#				else: #the data were getting is window data	
#					point = DataStream()
#					for i in range(1, len(valuesplit)):
#						point.window.append(float(valuesplit[i]))
#					STORAGE[id] = point
#			elif STORAGE[id].carcount == None and STORAGE[id].window != []: #case where window data somehow arrived before the actual data
#				STORAGE[id].carcount = int(valuesplit[0])
#				STORAGE[id].voltage = float(valuesplit[1])
#				STORAGE[id].temperature = float(valuesplit[2])
#				update.doPost(id, STORAGE[id].carcount, STORAGE[id].voltage, STORAGE[id].temperature, STORAGE[id].window)
#				del STORAGE[id]
#			elif STORAGE[id].carcount != None and STORAGE[id].window == []: #case where window data arrived later(most likely case)
#				for i in range(1, len(valuesplit)):
#					STORAGE[id].window.append(float(valuesplit[i]))
#				update.doPost(id, STORAGE[id].carcount, STORAGE[id].voltage, STORAGE[id].temperature, STORAGE[id].window)
#				del STORAGE[id]
#
#		else: #the id is not in STORAGE, so we have to create it
#			point = DataStream()
#			if valuesplit[0] != 'w': #if the first character isn't the identifier char, then were collecting the local count, voltage, and temperature
#				point.carcount = int(valuesplit[0])
#				point.voltage = float(valuesplit[1])
#				point.temperature = float(valuesplit[2])
#			else: #the data were getting is window data	
#				for i in range(1, len(valuesplit)):
#					point.window.append(float(valuesplit[i]))
#			STORAGE[id] = point
