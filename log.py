#!/usr/bin/env python3

import BMP280
import GPS
import csv
import time
import datetime
from picamera import PiCamera
gps = GPS.getGPS()

#collect altitude and temperature
altitude = BMP280.altitude
temperature = BMP280.temperatureF

#collect GPS
latitude = gps['latitude']
longitude = gps['longitude']
speed = gps['speed']
timestamp = gps['timestamp']
		
#write to log
row = [timestamp, latitude, longitude, altitude, speed, temperature]

with open('log.csv', 'a') as logFile:
    writer = csv.writer(logFile)
    writer.writerow(row)
logFile.close()

#capture image or video
camera = PiCamera()
picTimestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
if altitude < 18000:
	camera.start_preview()
	time.sleep(5)
	camera.capture('/home/pi/RaspberryPiBalloon/image ' + picTimestamp + '.jpg')
	camera.stop_preview()
else:
	camera.start_preview()
	camera.start_recording('/home/pi/RaspberryPiBalloon/video ' + picTimestamp + '.h264')
	time.sleep(30)
	camera.stop_recording()
	camera.stop_preview()

#check speed and altitude and send GPS coordinates
# if altitude < 500 && speed < 10
# 
# 	W_buff = ["AT\r\n", "AT+CMGF=1\r\n", "AT+CSCA=\"+8613800755500\"\r\n", "AT+CMGS=\"18825271704\"\r\n",str(latitude, longitude)]
# 	ser.write(W_buff[0])
# 	ser.flushInput()
# 	data = ""
# 	num = 0
# 
# 	try:
# 		while True:
# 			#print ser.inWaiting()
# 			while ser.inWaiting() > 0:
# 				data += ser.read(ser.inWaiting())
# 			if data != "":
# 				print data
# 				#if data.count("O") > 0 and data.count("K") > 0 and num < 3:	# the string have ok
# 				if num < 3:
# 					time.sleep(1)
# 					ser.write(W_buff[num+1])
# 				#if num == 3 and data.count(">") > 0:
# 				if num == 3:
# 					#print W_buff[4]
# 					time.sleep(0.5)
# 					ser.write(W_buff[4])
# 					ser.write("\x1a\r\n")# 0x1a : send   0x1b : Cancel send
# 				num =num +1
# 				data = ""
# 	except keyboardInterrupt:
# 		if ser != None:
# 			ser.close()
			
#turn on LoRa

    
    
# 
# crontab -e
# 
# * * * * * python3.4 /home/pi/log.py