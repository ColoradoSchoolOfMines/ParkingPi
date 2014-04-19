# Python script for the pi backend to post to website after getting XBee Data

import requests

# This method will post data from the Fio magnetometer to the ACMx server.
# It uses the 'requests' module for Multipart-Encoding of the image file. See 
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
	
	url = "http://acmxlabs.org/smartlots/fiodata" 
	
	# Construct normal form variables payload.
	dPayload = {
			"username": "wsn", 
			"password": "raspberryp1", 
			"id": sensorID,
			"carcount": carcount, 
			"voltage": battery, 
			"temperature": temperature,
			"window": window
	}
	
	# Create a requests object to handle all the urllib2 stuff.
	r = requests.post(url, data=dPayload)
	
	# Print out the server's response.
	print r.text


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
	
	url = "http://acmxlabs.org/smartlots/pidata"
	
	# Construct the file payload.
	fPayload = {"image": image}
	
	# Construct normal form variables payload.
	dPayload = {
			"username": "wsn", 
			"password": "raspberryp1", 
			"id": sensorID
	}
	
	# Create a requests object to handle all the urllib2 stuff.
	r = requests.post(url, data=dPayload, files=fPayload)
	
	# Print out the server's response.
	print r.text

