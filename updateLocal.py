def doPost(sensorID,carCount,battery) :
	print "posting:",carCount
	file=open("/var/www/index.php","w")
	urlcontent='<?php echo "php works";var_dump($_POST);?><html><body><h1>Hello! This the parking sensor project page!</h1>	<p>This is the default web page for this server.</p><p>The web server software is running but no content has been added, yet.</p>' + str(carCount) + '</body></html>'
	file.write(urlcontent)
	file.close()
