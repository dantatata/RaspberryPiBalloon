#!/usr/bin/env python3

import serial
import time
ser = serial.Serial("/dev/ttyS0", 115200)
ser.timeout=1
command = ["AT+CGNSPWR?\r\n", "AT+CGNSPWR=1\r\n", "AT+CGNSINF\r\n", "AT+CGNSPWR=0\r\n"]
gpsResponse = ''
attempts = 0
power = 0
fix = 0

while gpsResponse == '':
	if attempts == 50:
		ser.write(command[3])
		time.sleep(2)
		attempts = 0
	if power == 0:
		ser.write(command[0])
		response = ser.readline()
		while response.find('+CGNSPWR:') < 0:
			response = ser.readline()
		if response.find('+CGNSPWR: 1') > 0:
			power = 1
		if response.find('+CGNSPWR: 1') < 0:
			ser.write(command[1])	
			power = 1
	while fix == 0:
		ser.write(command[2])
		time.sleep(2)
		response = ser.readline()
		while response.find('+CGNSINF:') < 0:
			response = ser.readline()
		gpsResponse = response.split(',')	
		fix = gpsResponse[1]
	attempts = attempts+1
timestamp = gpsResponse[2]
latitude = gpsResponse[3]
longitude = gpsResponse[4]
altitude = gpsResponse[5]
speed = gpsResponse[6]	