#!/usr/bin/env python3

import serial
import time
ser = serial.Serial("/dev/ttyS0", 115200)
ser.timeout=1
command = ["AT+CGNSPWR?\r\n", "AT+CGNSPWR=1\r\n", "AT+CGNSINF\r\n", "AT+CGNSPWR=0\r\n"]
gpsStatus = 0
gpsPower = 0
gpsFix = 0

def getGPS():
	global gpsStatus
	global gpsPower
	global gpsFix
	global timestamp
	global latitude
	global longitude
	global speed
	attempts = 0
	resets = 0
	while gpsStatus == 0:
		if resets > 2:
			gpsResponse = 0
		if attempts == 50:
			ser.write(command[3])
			time.sleep(2)
			attempts = 0
			resets += 1
		if gpsPower == 0:
			ser.write(command[0])
			response = ser.readline()
			while response.find('+CGNSPWR:') < 0:
				response = ser.readline()
			if response.find('+CGNSPWR: 1') > 0:
				gpsPower = 1
			if response.find('+CGNSPWR: 1') < 0:
				ser.write(command[1])	
				gpsPower = 1
		while gpsFix == 0:
			ser.write(command[2])
			time.sleep(2)
			response = ser.readline()
			while response.find('+CGNSINF:') < 0:
				response = ser.readline()
			gpsResponse = response.split(',')	
			gpsFix = gpsResponse[1]
		attempts += 1
	if gpsResponse == 0:
		return "Unable to acquire signal"
	timestamp = gpsResponse[2]
	latitude = gpsResponse[3]
	longitude = gpsResponse[4]
	altitude = gpsResponse[5]
	speed = gpsResponse[6]	
