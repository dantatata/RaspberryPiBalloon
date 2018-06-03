#!/usr/bin/env python3

import serial
import time
ser = serial.Serial("/dev/ttyS0", 115200)
ser.timeout=1
command = ["AT+CGNSPWR?\r\n", "AT+CGNSPWR=1\r\n", "AT+CGNSINF\r\n", "AT+CGNSPWR=0\r\n"]
gpsPower = 0

def getGPS():
	global gpsPower
	global gpsFix
	global response
	if gpsPower == 0:
		ser.write(command[0])
		response = ser.readline()
		while response.find('+CGNSPWR:') < 0:
			response = ser.readline()
		if response.find('+CGNSPWR: 1') >= 0:
			gpsPower = 1
		if response.find('+CGNSPWR: 1') < 0:
			ser.write(command[1])	
			gpsPower = 1
			time.sleep(10)
	gpsFix = 0
	while gpsFix == 0:
		ser.write(command[2])
		time.sleep(2)
		response = ser.readline()
		while response.find('+CGNSINF:') < 0:
			response = ser.readline()
		gpsResponse = response.split(',')	
		gpsFix = gpsResponse[1]
	return {
	'timestamp' : gpsResponse[2],
	'latitude' : gpsResponse[3],
	'longitude' : gpsResponse[4],
	'altitude' : gpsResponse[5],
	'speed' : gpsResponse[6]}
