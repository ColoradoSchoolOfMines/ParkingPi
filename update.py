"""
Python script for the pi backend to curl post website after getting data xbee
"""

import urllib2
import urllib
#import xbee
#import serial

"""
doPost will take the data from recieve_asnycrounous_data and send the data to the website. It will encode for post.
returns the page for debuging and user convience
	
"""

"""
Temperature and pointWindow default to None so legacy code works
"""
def postFioData(sensorID, carcount,  battery, temperature=None, window=None):
	dataWindow = ""
	
	# Create data array
	data = [("id", sensorID), ("carcount", carcount), ("voltage", battery), ("temperature", temperature), ("window", window)]
	
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

def postPiData(sensorID, image):

	# Create data array
	data = [("id", sensorID)]

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

