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
# PM: modified march 2019
# Example: $ sudo python senderp_otaa.py 
#            Serial Port? /dev/ttyUSB0
#

import serial
import time
import datetime
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

# This command resets and restarts the RN2483 module; 
# stored internal configurations will be loaded automatically upon reboot
send_cmd(ser, b'sys reset')  

print('Setting channel parameters:')
send_cmd(ser, b'mac pause') # pauses the LoRaWAN stack functionality to allow transceiver configuration
send_cmd(ser, b'radio set pwr 14')
send_cmd(ser, b'radio set sf sf7')
# send_cmd(ser, b'radio set bw 250')
# send_cmd(ser, b'radio set freq 868100000')
send_cmd(ser, b'mac resume') # resumes the LoRaWAN stack functionality


if (DEBUGMODE>1):
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
# more infos on settind duty cycle here: https://www.microchip.com/forums/m947922.aspx#947922
# formula indicated in "RN2483module ug.pdf" page 29 
send_cmd(ser, b'mac set ch dcycle 0 9') # Sets the duty cycle to 10% 
send_cmd(ser, b'mac set ch dcycle 1 9') # Sets the duty cycle to 10% 
send_cmd(ser, b'mac set ch dcycle 2 9') # Sets the duty cycle to 10% 
# In Loriot get this data from the LoRaWAN Parameters section of the Device part of the console
# In TTN get this data from the DEVICE OVERVIEW of the console
send_cmd(ser, b'mac set appkey ___________________________')
# In Loriot get this data from the Device Details section of the Device part of the Loriot console
# In TTN get this data from the DEVICE OVERVIEW of the console
send_cmd(ser, b'mac set appeui ___________________________')
send_cmd(ser, b'mac save')
ser.write(b'mac join otaa'+'\r\n')
rval = ''
while "accepted" not in rval:
    rval = str(ser.readline())
    if (DEBUGMODE==1):
        print('Joining... got: '+rval)


try:
    kount = 0
    while kount<1000:

        cmd = "mac tx uncnf 1 "
        rawpayload = 'Hello '+str(kount)
        _length, _payload = packer.Pack_Str(rawpayload)

        if int(_length) < int(MAX_PAYLOAD_LENGTH):
            byte_rawcmd = bytes(cmd + _payload)

            print("Executing: "+byte_rawcmd[:-2]+ " at: " + str(datetime.datetime.now()))
            

            ser.write(byte_rawcmd)
            rval = ''
            while "mac_tx_ok" not in rval:
                rval = str(ser.readline())
                if (DEBUGMODE==1):
                    print('Executing: '+byte_rawcmd[:-2]+'... got: '+rval)
            if "mac_tx_ok" in rval:
                print("Sent: " + rawpayload+ " at: " + str(datetime.datetime.now()))
            else:
                print("Sending ERROR!")

            kount = kount+1
            # Consider duty cycle...
            time.sleep(30)


finally:
    ser.close()

