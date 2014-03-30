"""
Python script for the pi backend to curl post website after getting data xbee
"""

import urllib2
import urllib
#import xbee
#import serial

"""
doPost takes a int or string representing the carcount recived from the xbee, and a arduino id
and does a post to a specific webpage
returns the page for debuging and user convience
	
"""

"""
Temperature and pointWindow default to None so legacy code works
"""
def doPost(sensorID, carCount,  battery, temperature=None, window=None):
	dataWindow = ""
	
	data = [("%s" % (sensorID), "%s" % (carCount)),("%s" %(sensorID), "%s" % (battery)), ("%s" %(sensorID), "%s" %(temperature))] #make the key value pairs. 
	for point in window:
		data.append(("%s" %(sensorID), "%s" % (point)))
	encodedData = urllib.urlencode(data) #encode the data
	path = "http://acmxlabs.org/parking" #go to the acmxlabs website
	request = urllib2.Request(path, encodedData) # send request
	request.add_header("Content-type", "application/x-www-form-urlencoded") #add headers
	page = urllib2.urlopen(request) #get the page

	return page


