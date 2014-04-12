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
SENSORBUFFER = {} #stores the data until it gets its paired data

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

	"""
	Since XBee's will split the data along frames, we only want to send data to website once we have all the data
	To solve this, each data stream will end with a specific char, in this case it is '>'. 
	data streams will be 
	
		header_data < localcount voltage temperature window_data window_data window_data ... window_data >

	Occasionally debug statements will be sent. all debugs will be surronded by square brackets  [ ] 
	Debug statements will be only a single xbee frame, and no data statments will be in the same window as a debug statment
	therefore all debug statments will be ignored can simply have the entire stream thrown out
	debug statments will be

		header_data [ DEBUG_STATEMENT ... DEBUG_STATEMENT ]
	
	Because the entire data stream will not exist in a single XBee frame, when the id is extracted from the header,
	the stream will be added to a map. If there is already an id in the map, it will append the current frame into the data
	already in the dictonary
	When the terminating character is found (the > char) it will append the current frame to the one in the map and 
	then send the data in the map. The id will be removed from the map when the data is sent to site. 

	The name of the map is SENSORBUFFER and exists in global scope.

	"""
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
		#get the id, and make sure that there is data to grab
		id = ord(idstr[0]) * 256 + ord(idstr[1])
		if id in SENSORBUFFER: #case where were still recieving data
			if values.find("[") != -1: #there is a segment to ignore
				None #entire stream is debug, no data to get
			elif values.find(">") == -1: #not the end of data stream
				SENSORBUFFER[id] += values
			else:
				SENSORBUFFER[id] += values
				parseDataAndSend(id, SENSORBUFFER[id])
				del SENSORBUFFER[id]
		else: #new data recived for an id not in SENSORBUFFER
			SENSORBUFFER[id] = values
			
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
#		if id in SENSORBUFFER: #if the id is in SENSORBUFFER
#			if SENSORBUFFER[id] == None: #this is an extreme edge case, the id should never be added unless there was data before
#				if valuesplit[0] != 'w': #if the first character isn't the identifier char, then were collecting the local count, voltage, and temperature
#					point = DataStream()
#					point.carcount = int(valuesplit[0])
#					point.voltage = float(valuesplit[1])
#					point.temperature = float(valuesplit[2])
#					SENSORBUFFER[id] = point
#				else: #the data were getting is window data	
#					point = DataStream()
#					for i in range(1, len(valuesplit)):
#						point.window.append(float(valuesplit[i]))
#					SENSORBUFFER[id] = point
#			elif SENSORBUFFER[id].carcount == None and SENSORBUFFER[id].window != []: #case where window data somehow arrived before the actual data
#				SENSORBUFFER[id].carcount = int(valuesplit[0])
#				SENSORBUFFER[id].voltage = float(valuesplit[1])
#				SENSORBUFFER[id].temperature = float(valuesplit[2])
#				update.doPost(id, SENSORBUFFER[id].carcount, SENSORBUFFER[id].voltage, SENSORBUFFER[id].temperature, SENSORBUFFER[id].window)
#				del SENSORBUFFER[id]
#			elif SENSORBUFFER[id].carcount != None and SENSORBUFFER[id].window == []: #case where window data arrived later(most likely case)
#				for i in range(1, len(valuesplit)):
#					SENSORBUFFER[id].window.append(float(valuesplit[i]))
#				update.doPost(id, SENSORBUFFER[id].carcount, SENSORBUFFER[id].voltage, SENSORBUFFER[id].temperature, SENSORBUFFER[id].window)
#				del SENSORBUFFER[id]
#
#		else: #the id is not in SENSORBUFFER, so we have to create it
#			point = DataStream()
#			if valuesplit[0] != 'w': #if the first character isn't the identifier char, then were collecting the local count, voltage, and temperature
#				point.carcount = int(valuesplit[0])
#				point.voltage = float(valuesplit[1])
#				point.temperature = float(valuesplit[2])
#			else: #the data were getting is window data	
#				for i in range(1, len(valuesplit)):
#					point.window.append(float(valuesplit[i]))
#			SENSORBUFFER[id] = point
