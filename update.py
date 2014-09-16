# Python script for the pi backend to post to website after getting XBee Data

import requests

# This method will post data from the Fio magnetometer to the ACMx server.
# It uses the 'requests' module for encoding of the form fields. See 
# http://docs.python-requests.org/ for documentation. Prints server response
# to the console.
# 
# Args:
#		sensorID: The ID of the sensor who recorded the image.
#		carcount: The reported count of vehicles from the Fio.
#		battery: The battery level of the Fio (float).
#		temperature: set to None for legacy compatibility.
#		window: set to None for legacy compatibility.
#
#	Returns:
#		(nothing)
# 
def postFioData(sensorID, carcount,  battery, temperature=None, window=None):
	
	url = "http://wsn:raspberryp1@acmxlabs.org/smartlots/fiodata" 
	#since requests won't send an array, we need to convert array to single string
	windowDataAsSingleString = ""
	for entry in window:
		windowDataAsSingleString += entry
		windowDataAsSingleString += " "

	#remove trailing space, this saves a byte on every xbee transimission
	windowDataAsSingleString = windowDataAsSingleString[:-1] 
	# Construct normal form variables payload.
	dPayload = {
			"id": sensorID,
			"carcount": carcount,
			"voltage": battery,
			"temperature": temperature,
			"window": windowDataAsSingleString
	}
	
	# Create a requests object to handle all the urllib2 stuff.
	r = requests.post(url, data=dPayload)
	
	# Print out the server's response.
	print r.text




















"""Depricated, There is no reason to post pi data if there is no pi
# This method will post an image to the ACMx server. It uses the 'requests'
# module for Multipart-Encoding of the image file. See 
# http://docs.python-requests.org/ for documentation. Prints server response
# to the console.
# 
# Args:
#		sensorID: The ID of the sensor who recorded the image.
#		image: A file handle that was opened for binary reading.
#					e.g. f = open('img.png', 'rb')
#
#	Returns:
#		(nothing)
# 
def postPiData(sensorID, image):
	
	url = "http://wsn:raspberryp1@acmxlabs.org/smartlots/pidata"
	
	# Construct the file payload.
	fPayload = {"image": image}
	
	# Construct normal form variables payload.
	dPayload = {
			"id": sensorID
	}
	# Create a requests object to handle all the urllib2 stuff.
	r = requests.post(url, data=dPayload, files=fPayload)
	
	# Print out the server's response.
	print r.text
"""
