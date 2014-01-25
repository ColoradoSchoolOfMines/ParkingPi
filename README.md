ParkingPi
=========

The code for the raspberry Pi specfic to the Parking Sensor project

If you want the pi to text you the ip address, you have to 
1. Have a twillo account
2. Have an apache server running(doesn't need to have connection outside of localhost)
3. add your number to the array of numbers(Please remove the numbers of people currently not using that pi)
4. copy YoIpAddressFo folder into /var/www
5. add smsbootscript to startup(google it, there are lots of ways to do this)


description of files:
wattcher.py: Master script, run this with a sensor pluged in and it will handle the rest

update.py: This is the script that will update the server when it finally gets up. 

datachecker.py: This file will take a string of data from the receiver and check to see if it is formated properly. 

updateLocal.py: like update.py but uses a local web server and writes the html through python. Use this instead of update.py when the server is not up.

smsbootscript.sh: a very roundabout way of getting the pi to text you the ip address after 30 seconds from being intiated. see above to make it work for your pi

YoIpAddressFoo: files all related to the smsbootscript. ingore these if you don't use smsbootscript.sh or you have a USB hub


