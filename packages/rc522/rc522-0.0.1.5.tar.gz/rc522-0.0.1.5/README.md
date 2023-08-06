## Context

This tool is showcased in the project [IotaWorkshop](https://github.com/Tsangares/iotaworkshop)

# Summary

This is a basic RFID libarary for the rc522. This simply lets you pull a single tag data and later lets you confirm it using the function `detectKey(uid,block)`

# Installation

This package requires `RPi.GPIO`, which I installed on arch arm using

    yay -S python-raspberry-gpio
	
But ubuntu or rasbian can use,

    pip install RPi.GPIO

To install pibeep simply install the pip package.

    pip install rc522


# Example
Simple example of usage 

	from rc522 import detect,detectKey
	uid,block detect(rst=31,irq=29)
	#Later you can check that the same raid tag is still there using
	if detectKey(uid,block,rst=31,irq=29):
		print("RFID tag is still there")
	else:
		print("RFID tag is vacant!")
		

## Wiring
To connect the RC522 module to SPI use the following schematic. [Use this pinout diagram](http://pi.gadgetoid.com/pinout) for reference.

| Board pin name | Board pin | Physical RPi pin | RPi pin name | 
|----------------|-----------|------------------|--------------|
| SDA            | 1         | 24               | GPIO8, CE0   | 
| SCK            | 2         | 23               | GPIO11, SCKL | 
| MOSI           | 3         | 19               | GPIO10, MOSI | 
| MISO           | 4         | 21               | GPIO9, MISO  | 
| IRQ            | 29        |                  | GPIO5        | 
| GND            | 6         | 6, 9, 20, 25     | Ground       | 
| RST            | 31        |                  | GPIO6        | 
| 3.3V           | 8         | 1,17             | 3V3          | 
