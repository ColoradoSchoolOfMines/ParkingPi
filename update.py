# Python script for the pi backend to post to website after getting XBee Data

import urllib2
import urllib
import hashlib

# Temperature and pointWindow default to None so legacy code works

# Posts the data from the fio magnetometer sensors to the acmx server
def postFioData(sensorID, carcount,  battery, temperature=None, window=None):
	dataWindow = ""
	
	# Create data array
	data = [("username", "wsn"), ("password", "raspberryp1"), ("id", sensorID), ("carcount", carcount), ("voltage", battery), ("temperature", temperature), ("window", window)]
	
	# Encode the data
	encodedData = urllib.urlencode(data)

	# HTTP url
	path = "http://acmxlabs.org/smartlots/fiodata" 

	# Create request
	request = urllib2.Request(path, encodedData)

	# Add headers
	request.add_header("Content-type", "application/x-www-form-urlencoded") 
	
	# Send request
	page = urllib2.urlopen(request)

	print page.read()

	return page 


# Posts the data from the image acquisition Pis to the acmx server
def postPiData(sensorID, image):

	# Create data array
	data = [("username", "wsn"), ("password", "raspberryp1"), ("id", sensorID)]

	# Encode the data
	encodedData = urllib.urlencode(data)

	# HTTP url
	path = "http://acmxlabs.org/smartlots/pidata"

	# Create request
	request = urllib2.Request(path, encodedData)

	# Add headers
	request.add_header("Content-type", "application/x-www-form-urlencoded")

	# Send request
	page = urllib2.urlopen(request)

	print page.read()

	return page

