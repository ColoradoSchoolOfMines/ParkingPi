#! /usr/bin/python

"""
receive_samples_async.py

By Paul Malmsten, 2010
pmalmsten@gmail.com

This file reads from the serial port and asynchronously processes the data
received from a remote XBee.
"""

from xbee import XBee
import time
import serial
import update

PORT = '/dev/ttyUSB0'
BAUD_RATE = 57600

# A dictionary (map) that stores the Fio packets, with each packet 
# in the map growing until the full data is received
FIO_DATA_BUFFER = {}

# A dictionary (map) that stores the Pi packets, with each packet 
# in the map growing until the full image is received
PI_DATA_BUFFER = {}

# A dictionary that stores the lengths of each image sent by the Pis
PI_STREAM_LENGTHS = {}

# Open serial port
#ser = serial.Serial(PORT, BAUD_RATE)

# Takes a data stream from a Fio and sends it to the server for storage
def parseFioDataAndSend(sensorId, dataStream):
	# Remove the < and > from of datastream
	dataStream = dataStream.replace("<", "")
	dataStream = dataStream.replace(">", "")

	valuesplit = dataStream.split()
	carcount = valuesplit[0]
	voltage = valuesplit[1]
	temperature = valuesplit[2]
	window = valuesplit[3:]
	update.postFioData(sensorId, carcount, voltage, temperature, window)

# Takes a data stream from a Pi and sends it to the server for storage
def parsePiDataAndSend(sensorId, dataStream):
	f = open("kitten.jpeg", "rb")
	update.postPiData(sensorId, f)

"""
The following function 'message_received(dataPacket)' is described below:
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

The name of the map is FIO_DATA_BUFFER and exists in global scope.
"""

def message_received(dataPacket):

	print dataPacket
	try :
		
		# Get the actual data payload we want to look at
		sensorPayload = dataPacket["rf_data"]

		if hackyMethodToIdentifyData(sensorPayload) == "pi":
			processPiMessage(dataPacket)

		elif hackyMethodToIdentifyData(sensorPayload) == "fio":
			processFioMessage(dataPacket)
	
	except Exception as e:
		# The last steps will fail for messages such as on calibration, we need to catch this
		pass	

def processPiMessage(dataPacket):

	sensorId = getSensorId(dataPacket)

	# Get the actual data payload we want to look at
	sensorPayload = dataPacket["rf_data"]	

	# Already received at least one packet for this sensor, so we will
	# add this data to the existing value in the map
	if sensorId in PI_DATA_BUFFER:

		# If the stream is still smaller than the specified length
		if len(PI_DATA_BUFFER[sensorId]) < PI_STREAM_LENGTHS[sensorId]:
			
			# Append this payload to the end of the stream
			PI_DATA_BUFFER[sensorId] += sensorPayLoad

			# Check to see the new length. If it's >= the specified length,
			# we know we have reached the end of the image stream
			if len(PI_DATA_BUFFER[sensorId]) == PI_STREAM_LENGTHS[sensorId]:
				parsePiDataAndSend(sensorId, PI_DATA_BUFFER[sensorId])
				del PI_DATA_BUFFER[sensorId]

			if len(PI_DATA_BUFFER[sensorId]) > PI_STREAM_LENGTHS[sensorId]:
				print("Error: Sensor " + sensorId + " sent the wrong number of image packets")
				exit()
		
		else:
			print("Error: Sensor " + sensorId + " sent the wrong number of image packets")
			exit()
				
	else:
		streamLength = int(sensorPayload[0:sensorPayload.find(" ")])
		firstPacket = sensorPayload[sensorPayload.find(" ") + 1:]

		PI_DATA_BUFFER[sensorId] = firstPacket
		PI_STREAM_LENGTHS[sensorId] = streamLength


def processFioMessage(dataPacket):

	sensorId = getSensorId(dataPacket)

	# Get the actual data payload we want to look at
	sensorPayload = dataPacket["rf_data"]

	# Remove dangerous characters
	sensorPayload = sensorPayload.replace("\r", "").replace("\n", "")

	# Already received at least one packet for this sensor, so we will
	# add this data to the existing value in the map
	if sensorId in FIO_DATA_BUFFER:
		
		# If this payload contains a '[', it means that this statement
		# is all debug info, so we ignore it
		if sensorPayload.find("[") != -1: 
			None
		
		# Check that this payload is not the last packet in the stream
		elif sensorPayload.find(">") == -1: 
			FIO_DATA_BUFFER[sensorId] += sensorPayload
		
		# If it is the last packet in the stream
		else:
			# Append the last payload
			FIO_DATA_BUFFER[sensorId] += sensorPayload
			# Send the entire stream to the server for storage
			parseFioDataAndSend(sensorId, FIO_DATA_BUFFER[sensorId])
			# Delete the data that was just sent to save space
			del FIO_DATA_BUFFER[sensorId]

	# This is the first packet from this sensor, so we create a new
	# entry in the map, with the sensorId as the key, payload as the value
	else:
		# If this payload contains a '[', it means that this statement
		# is all debug info, so we ignore it
		if sensorPayload.find("[") != -1:
			None
		else:
			FIO_DATA_BUFFER[sensorId] = sensorPayload		

def getSensorId(dataPacket):
	# Grab hex string representing sensor id, it's given as a raw binary number
	sensorIdHex = dataPacket["source_addr"]

	# Get the actual sensor id, and make sure that there is data to grab
	sensorId = ord(sensorIdHex[0]) * 256 + ord(sensorIdHex[1])

	return sensorId

def hackyMethodToIdentifyData(sensorPayload):

	print("Currently using hacky method. Please update as soon as possible. Let's not be lazy here. Seriously though. FIX IT!")

	isFio = True
	for char in sensorPayload.replace("<", ""):
		if not (ord(char) == ord(' ') or ord(char) == ord('.') or ord(char) == ord('>') or (ord(char) in range(ord('0'), ord('9') + 1))):
			isFio = False
			break

	if isFio:
		return "fio"
	else:
		return "pi"

testDataStream = "<200 4.7 50 10.1 10.2 10.3 10.4 10.5 10.6 10.7 10.8 10.9>"
parseFioDataAndSend(7, testDataStream)

testPiStream = "102400 as;ofijw9r8uapw9erjas jdfzsdjf jawli,,.fhxfglq8uw3498ysf#R$**9hdfsaehrksdf;sfawr68569#$("
parsePiDataAndSend(3, testPiStream)

# Create API object, which spawns a new thread
# xbee = XBee(ser, callback=message_received)

# Do other stuff in the main thread
# while True:
#    try:
#        time.sleep(.1)
#    except KeyboardInterrupt:
#        break

# halt() must be called before closing the serial
# port in order to ensure proper thread shutdown
# xbee.halt()
# ser.close()
