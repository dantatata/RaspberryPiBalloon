#!/usr/bin/env python3

import serial
import time
ser = serial.Serial("/dev/ttyS0", 115200)
ser.timeout=1
def poweronGPS():
	ser.write("AT+CGNSPWR?\r\n")
	response = ser.readline()
	while response.find('+CGNSPWR:') < 0:
		response = ser.readline()
	if response.find('+CGNSPWR: 1') < 0:
		ser.write("AT+CGNSPWR=1\r\n")
def queryGPS():
	ser.write("AT+CGNSINF\r\n")
	time.sleep(2)
	response = ser.readline()
	while len(response) < 20:
		response = ser.readline()
	splitresponse = response.split(',')
	return splitresponse
def getFix():
	gpsResponse = queryGPS()
	while gpsResponse[1] == '0':
		time.sleep(5)
		gpsResponse = queryGPS()
poweronGPS()
getFix()
gpsResults = queryGPS()
timestamp = gpsResults[2]
latitude = gpsResults[3]
longitude = gpsResults[4]
altitude = gpsResults[5]
speed = gpsResults[6]		