#!/usr/bin/env python
""" 
Turns out that the xbee data frames can only feasibly be sent if you also use a python module to send them, and since the aurdino does not use python, it would be a lot of work to 'pretend' to be sending it from the python library
xbee data frame only created from python xbee library
"""
#dummy dictonaries, replace these with actual data on deploy
idToLot = {'0':'lowerCTLM', '1':'lowerCTLM', '2':'upperCTLM', '3':'upperCTLM', '4':'oLot'}
idToCar = {'0':23, '1':-5, '2':56, '3':20, '4':15}
lotToCar= {'lowerCTLM':18, 'upperCTLM':76, 'oLot':15}
import serial, time, datetime, sys, dataChecker, update, updateLocal
#from xbee import XBee

# use App Engine? or log file? comment out next line if appengine
LOGFILENAME = "Sensordatalog.csv"   # where we will store our flatfile data

# open up the FTDI serial port to get data transmitted to xbee
print "opening serial port"
serial_port = serial.Serial("/dev/ttyUSB0", 57600)
print "opened serial port"
#xbee = XBee(serial_port)
def readFromSerial(serial_port):
	while True:
		try:
			readData = serial_port.next()
			readData = readData.strip()
			print readData
			dataChecker.debug = True
			print "entering dataChecker"
			returnedData = dataChecker.checkData(readData) #this may return None if data checker thinks the data is corrupted
			print "exited dataChecker"
			if returnedData is not None:
				dataSplit = returnedData.split(":")

				#print update.doPost(dataSplit[0], dataSplit[1], dataSplit[2]).read()
				#simplified version using a local apache server
				print "trying to post:", dataSplit
				print updateLocal.doPost(dataSplit[0], dataSplit[1], dataSplit[2])
			#print "Sent data"

			print returnedData
			""" 
			current idea of how data will be parsed
			"""
			#parseData(serial_port.next())
			
			#print xbee.wait_read_frame()
		except KeyboardInterrupt:
			break
	serial_port.close()

#assumes debug statments are suppresed, so aurdino only sends key:value pairs
def parseData(data):
	dataList = data.split(":")
	sensorId = dataList[0]
	carCount = int(dataList[1])
	#turn sensor id into correct parking lot
	parkingLot = idToLot[sensorId]
	#update the number that the sensor has
	idToCar[sensorId] = carCount
	lotToCar[parkingLot] = 0
	for key,value in idToLot.items():
		if value == parkingLot:
			lotToCar[value] += idToCar[key]
"""		
for key,value in lotToCar.items():
	print "%s %i" % (key, value)
print "\n"
parseData('1:23')
for key,value in lotToCar.items():
	print"%s %i" % (key, value)	
parseData('1:-5')

for key,value in lotToCar.items():
	print"%s %i" % (key, value)	
print "\n"
parseData('4:32')
for key,value in lotToCar.items():
	print"%s %i" % (key, value)	


"""
print "about to read"
readFromSerial(serial_port)
