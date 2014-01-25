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
def doPost(carCount, sensorID, battery):
	carCount = [("%s" % (sensorID), "%s" % (carCount)),("%s" %(sensorID), "%s" % (battery))]
	encodedData = urllib.urlencode(carCount)
	path = "http://parking.mines.edu/index.php" #TODO make real webpage
	request = urllib2.Request(path, encodedData)
	request.add_header("Content-type", "application/x-www-form-urlencoded") #TODO may need to modify header
	page = urllib2.urlopen(request)

	return page


