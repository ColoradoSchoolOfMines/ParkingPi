"""
PLEASE UPDATE THE AUTHORS COMMENT AT BOTTOM OF CODE IF YOU MODIFY
This is primarly to keep tabs on who works on it without having to look at git commit logs
"""
"""
This is an idea for the implementation of the pi for returning a proper string or None type if it suspects there is corruption

"""
#Change this variable to True if you want debug statments to appear during parsing
debug = False

#takes a string of id:carcount:battery:checksum; and either returns the id:carcount:battery part or None if the data must be thrown out
def checkData(inputString):
	global debug
	#last character is not the ;
	try:
		if inputString[-1] != ';':
			if debug:
				print "Rejected because of missing semicolon"
			return None

		if inputString.count(';') != 1:
			if debug:
				print "Rejected because of too many semicolons"
			return None
		if inputString.count('!') != 1:
			if debug:
				print "Rejected because of improper amount of !"
			return None


		splitString = inputString.split('!')
		checkSum = int(splitString[1][:-1])
		if checkSum != len(splitString[0]):
			if debug:
				print "Rejected because of checksum mismatch"
			return None
		subSplitString = splitString[0].split(":")
		if len(subSplitString) != 3:
			if debug:
				print "Rejected because of improper amount of colons(':')"
			return None
		else:
			if debug:
				print "Data is formated properly"
			data = "%s:%s:%s" % (subSplitString[0], subSplitString[1], subSplitString[2])
			return data

	except ValueError as e:
		if debug:
			print "Rejected because of int conversion error on checksum"	
		return None


"""

	splitString = inputString.split(':')

	#see if there are not 4 :'s
	if len(splitString) != 4:
		if debug:
			print "Rejected because of improper splitString length"
		return None

	#see if there are multiple semicolons in data
	if inputString.count(';') != 1:
		if debug:
			print "Rejected because of multiple semicolons"
		return None

	#capture the checksum value
	checkSum = int(splitString[3][:-1]) #removes the ;

	#see if the checksum and stringlength match
	if len(inputString) != checkSum:
		if debug:
			print "Rejected because of checksum mismatch"
		return None

"""
	#At this point, our data appears to be valid in terms of format
	#do note that it is still possible to have corrupted data, but the odds of getting corrupted data that is properly formated is very low. These cases can be accounted for later in wattcher code if need be. 
"""
Function for testing and debug
"""
def testCheckString():
	global debug
	#extra layer incase someone(aka drew) forgets to remove a testCheckString() function call in final version, there will not be debug statments all over the place
	if debug:
		print "Testing: format is inputed \\n expected \\n result"
		test = "1:45:87:11;"
		expected = "1:45:87"
		result = checkData(test)
		print test
		print expected
		if result == None:
			print "Rejected data"
		else:
			print result
	
		print ""
		
		test = "1:45:87:11:;"
		expected = "Rejected data"
		result = checkData(test)
		print test
		print expected
		if result == None:
			print "Rejected data"
		else:
			print result
	
		print ""
		
		test = "1:45:87;"
		expected = "Rejected data"
		result = checkData(test)
		print test
		print expected
		if result == None:
			print "Rejected data"
		else:
			print result
		
		print ""
	
		test = "1:45:87:10;"
		expected = "Rejected data"
		result = checkData(test)
		print test
		print expected
		if result == None:
			print "Rejected data"
		else:
			print result
	
		print ""
		
		test = "17:4:7:9;"
		expected = "17:4:7"
		result = checkData(test)
		print test
		print expected
		if result == None:
			print "Rejected data"
		else:
			print result
		print ""
	
		test = "17:4:7:8"
		expected = "Rejected data"
		result = checkData(test)
		print test
		print expected
		if result == None:
			print "Rejected data"
		else:
			print result
	


"""
This is a list of people who have contributed/edited/debuged/optimized this particular code/algorithms for dectecting corrupt data
CURRENT AUTHORS:
	Drew Koelling
"""
