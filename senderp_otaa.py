#!/usr/bin/python
# -*- coding: UTF-8 -*-
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# Copyright (c) 2016, raspberrypi.com.tw
# All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# sender.py
# A demo program for lora to send message compatible with python2/3
#
# Author : sosorry
# Date   : 08/06/2016
#
# Example: $ sudo python sender.py 
#            Serial Port? /dev/ttyUSB0
#
# Modified by PM: 7feb2019
# execute also as: python sender.py /dev/ttyUSB0

import serial
import time
import re
import json
import packer

import sys

DEBUGMODE = 1

MAX_PAYLOAD_LENGTH = 121

def send_cmd(serchan, thecmd):
    serchan.write(thecmd+'\r\n')
    returned_msg = str(serchan.readline())
    if (DEBUGMODE==1):
        print('sent cmd: '+thecmd+" -> got: "+returned_msg)

#
# start here
#

try:
    input = raw_input
except NameError:
    pass

if (len(sys.argv) != 2): 
    serial_port = input("Serial Port? ")
else:
    serial_port = sys.argv[1]
print("using port: ", serial_port)

# open up the FTDI serial port to get data transmitted to lora
BAUDRATE = 57600               # the baud rate we talk to the microchip RN2483
ser = serial.Serial(serial_port, BAUDRATE)
if ser.isOpen() == False:
    ser.open()
# The default settings for the UART interface are 
# 57600 bps, 8 bits, no parity, 1 Stop bit, no flow control. 
ser.bytesize = 8
ser.parity   = "N"
ser.stopbits = 1
ser.timeout  = 5

print('Setting channel parameters:')
send_cmd(ser, b'radio cw off')  # Disabling Continuous Wave (CW) mode. Semantically identical to "sys reset"
send_cmd(ser, b'radio set pwr 14')
send_cmd(ser, b'radio set bw 250')
send_cmd(ser, b'radio set freq 868100000')
send_cmd(ser, b'radio set sf sf7')


print('Getting channel parameters:')

send_cmd(ser, b'radio get bt')
send_cmd(ser, b'radio get mod')
send_cmd(ser, b'radio get freq')
send_cmd(ser, b'radio get pwr')
send_cmd(ser, b'radio get sf')
send_cmd(ser, b'radio get afcbw')
send_cmd(ser, b'radio get bitrate')
send_cmd(ser, b'radio get fdev')
send_cmd(ser, b'radio get prlen')
send_cmd(ser, b'radio get crc')
send_cmd(ser, b'radio get iqi')
send_cmd(ser, b'radio get cr')
send_cmd(ser, b'radio get wdt')
send_cmd(ser, b'radio get bw')


# Using OTAA
print('Setting LoRaWAN parameters:')
# In Loriot get this data from the LoRaWAN Parameters section of the Device part of the console
# In TTN get this data from the DEVICE OVERVIEW of the console
send_cmd(ser, b'mac set appkey ___________________________')
send_cmd(ser, b'mac save')
# In Loriot get this data from the Device Details section of the Device part of the Loriot console
# In TTN get this data from the DEVICE OVERVIEW of the console
send_cmd(ser, b'mac set appeui ___________________________')
send_cmd(ser, b'mac join otaa')


# pauses the LoRaWAN stack functionality to allow transceiver (radio) configuration
# must be called before any radio transmission or reception
send_cmd(ser, b'mac pause')

try:
    kount = 0
    while kount<1000:

        rawinput = 'Hello from pietro '+str(kount)

        try:
            byte_rawinput = bytes(rawinput + "\r\n")
        except:
            byte_rawinput = bytes(rawinput + "\r\n", encoding="UTF-8")

        cmd = "mac tx uncnf 1 "
        _length, _payload = packer.Pack_Str(rawinput)

        if int(_length) < int(MAX_PAYLOAD_LENGTH):
            print("Time: " + str(time.ctime()))
            byte_rawinput = bytes(cmd + _payload)
            ser.write(byte_rawinput)
            ser.readline()

            kount = kount+1
            time.sleep(5)
            print("Sent: " + rawinput)


finally:
    ser.close()

