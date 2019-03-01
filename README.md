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

### Support files:
* ```miniterm.py```: used to connect to a LoStick and send commands manually
* ```packer.py```: support file

### file: ```sender.py```
- sends a text message red from input
- execute as: ```python sender.py _lostik-serial-port_```

### file: ```senderp.py```
- periodically sends a text message stored in variable "rawinput"
- execute as: ```python senderp.py _lostik-serial-port_```
