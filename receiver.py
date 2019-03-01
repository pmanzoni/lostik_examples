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
# receiver.py
# A demo program for lora to receive message compatible with python2/3
#
# Author : sosorry
# Date   : 08/06/2016
#
# Example: $ sudo python receiver.py
#            Serial Port? /dev/ttyAMA0
#
# Modified by PM: 7feb2019
# execute also as: python receiver.py /dev/ttyUSB0

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

    return returned_msg


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
print(serial_port)

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
# Disabling Continuous Wave (CW) mode. This command is semantically identical to "sys reset"
send_cmd(ser, b'radio cw off')
send_cmd(ser, b'radio set pwr 14')
send_cmd(ser, b'radio set bw 250')
send_cmd(ser, b'radio set freq 868100000')
send_cmd(ser, b'radio set sf sf7')

# pauses the LoRaWAN stack functionality to allow transceiver (radio) configuration
# must be called before any radio transmission or reception
send_cmd(ser, b'mac pause')

send_cmd(ser, b'radio set wdt 0')

print('starting....')

try:
    while True:
        ret = send_cmd(ser, b'radio rx 0')

        if ret == "ok" or "radio_tx_ok" :

            payload = ser.readline()

            if (len(payload) > 0 and DEBUGMODE > 1):
            	print("raw payload: " + payload)

            if re.match('^radio_rx', str(payload).strip()):
                data = payload.split("  ", 1)[1]
                print("data >" + data[0:-2].decode("hex") + "<")

                print("Time: " + str(time.ctime()))
                send_cmd(ser, b'radio get snr')

                time.sleep(2)
        else:
        	print("WARNING: ", ret)


finally:
    ser.close()

