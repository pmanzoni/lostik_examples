# LoStik code examples
This repository contains code examples in Python to use with the LoStik device.

LoStick is a open source USB LoRa® device available here https://www.crowdsupply.com/ronoth/lostik. Its main characteristics are:
* Works with any PC, Raspberry Pi, or BeagleBone
* Simple ASCII interface
* Supports Packet mode LoRa® (packet mode) or LoRaWAN™
* Compatible with The Things Network and Loriot
* Based on the RN2903/R2483 by Microchip

**Main references used**
* The example here are basically based on those in: https://github.com/lolsborn/LoStik
* Some help also from here: https://github.com/raspberrypi-tw/lora

## Code examples

**senderp.py** 
- periodically send a text message stored in variable "rawinput"
- execute as: python senderp.py _/dev/tty..._