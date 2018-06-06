#!/usr/bin/env python3

import serial
import time
import os
ser = serial.Serial("/dev/ttyS0", 115200)
ser.timeout=1
command = ["AT\r\n", "AT+CMGF=1\r\n", "AT+CSCA=\"+12063130004\"\r\n", "AT+CMGS=\"+16086285197\"\r\n", "AT+CMGL=ALL\r\n", "AT+CMGD=ALL\r\n"]

def send(str):
	serialStatus = 0
	attempts = 0
	while serialStatus = 0:
		if attempts > 10:
			os.system('sudo reboot now')
		ser.write(command[0])
		time.sleep(1)
		response = ser.readline()
		while response.find('AT') >= 0:
			response = ser.readline()
		if response.find('OK') >= 0:
			serialStatus = 1
		attempts += 1
	ser.write(command[1])
	time.sleep(1)
	ser.write(command[2])
	time.sleep(1)
	ser.write(command[3])
	time.sleep(1)
	ser.write(str)
	ser.write("\x1a\r\n")

def receive():
	ser.write(command[4])
	time.sleep(2)
	response = ser.readline()
	while response.find('CMGR') >= 0:
		response = ser.readline()
	ser.write(command[5])
	return response

