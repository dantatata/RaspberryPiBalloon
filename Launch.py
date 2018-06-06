#!/usr/bin/env python3

import BMP280
import GPS
import SMS
import csv
import time
import datetime
from picamera import PiCamera
missionActive = 1
smsActive = 0

while missionActive == 1:
	bmp = BMP280.BMP280()
	gps = GPS.getGPS()

	#collect altitude and temperature
	bmpAltitude = bmp.altitudeF
	temperature = bmp.temperatureF

	#collect GPS
	latitude = gps['latitude']
	longitude = gps['longitude']
	speed = gps['speed']
	previousTimestamp = timestamp
	timestamp = gps['timestamp']
	gpsAltitudeMeters = gps['altitude']
	gpsAltitudeFeet = gpsAltitudeMeters * 3.2808

	#pick altitude reading
	if abs(bmpAltitude - gpsAltitudeFeet) > 200 or  gpsAltitudeFeet > 10000:
		altitude = gpsAltitudeFeet
	else:
		altitude = bmpAltitude
	
	#check for requests and commands
	if smsActive == 1:
		receivedSMS = SMS.receive()
		if receivedSMS.find('SPEED') >= 0:
			SMS.sendSMS(speed)
		if receivedSMS.find('ALTITUDE') >= 0:
			SMS.sendSMS(altitude)
		if receivedSMS.find('STOP') >= 0:
			sendSMS = 0
		if receivedSMS.find('ABORT') >= 0:
			missionActive = 0
	
	#pause
	elapsedTime = float(timestamp) - float(previousTimestamp)
	if elapsedTime < 200
		sleeptime = 120 - (elapsedTime * 60 / 100)
		time.sleep(sleeptime)
				
	#write to log
	row = [timestamp, latitude, longitude, bmpAltitude, gpsAltitudeFeet, speed, temperature]

	with open('log.csv', 'a') as logFile:
		writer = csv.writer(logFile)
		writer.writerow(row)
	logFile.close()

	#capture image or video
	camera = PiCamera()
	if altitude < 18000:
		camera.start_preview()
		time.sleep(5)
		camera.capture('/home/pi/RaspberryPiBalloon/image ' + timestamp + '.jpg')
		camera.stop_preview()
	if altitude > 18000:
		camera.start_preview()
		camera.start_recording('/home/pi/RaspberryPiBalloon/video ' + timestamp + '.h264')
		time.sleep(30)
		camera.stop_recording()
		camera.stop_preview()

# 	#check speed and altitude and send GPS coordinates
# 	sendSMS = 1
# 	if altitude < 1000 and speed < 10 and sendSMS = 1:
# 		gpsCoordinates = str(latitude) + 'N, ' + str(longitude) + 'W'
# 		SMS.send(gpsCoordinates)
# 		smsActive = 1
# 
# 
# 	#turn on LoRa
# 	loraMsg = lora.receive()
# 	if loraMsg['Success'] = 1
# 		lora.send('Online')
# 	lora.send(gpsCoordinates)
# 	previousRSSI = RSSI
# 	RSSI = loraMsg['RSSI']
# 	if RSSI > previousRSSI:
# 		lora.send('Warmer!')
    
    
# 
# crontab -e
# 
# * * * * * python3.4 /home/pi/log.py