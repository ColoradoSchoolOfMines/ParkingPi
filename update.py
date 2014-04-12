"""
Python script for the pi backend to curl post website after getting data xbee
"""

import urllib2
import urllib
import hashlib
#import xbee
#import serial

"""
doPost will take the data from recieve_asnycrounous_data and send the data to the website. It will encode for post.
returns the page for debuging and user convience
	
"""

"""
Temperature and pointWindow default to None so legacy code works
"""
def doPostFio(sensorID, carcount,  battery, temperature=None, window=None):
	password = hashlib.md5()
	password.update("raspberryp1")
	data = [("username", "wsn"), ("password", "raspberryp1"), ("id", sensorID), ("carcount", carcount), ("voltage", battery), ("temperature", temperature), ("window", window)]
	encodedData = urllib.urlencode(data) #encode the data
	path = "http://acmxlabs.org/smartlots/fiodata" #go to the acmxlabs website
	request = urllib2.Request(path, encodedData) # send request
	request.add_header("Content-type", "application/x-www-form-urlencoded") #add headers
	page = urllib2.urlopen(request) #get the page

	print page.read()

	return page


