# ADC6Click

This project implements a Python 3 driver for the MikroElectronica ADC 6 Click board that uses the AD7214-8 24 bit ADC.

## To Do
1. Read the ID register.
2. Write to a register
3. Configure ADC for read



## Concepts
The AD7124 has the following key concepts.

* SPI communications are mode 3.
* All communications begin by writing one byte to the communications 
register.
* The ID register is used to verify the device type.
* There are 16 channels that can use any one of 8 setups.


## ADC 6 Click Connections

This table shows the connections from the AD7124 to Raspberry Pi via the
mikroBUS™ socket and the Pi2 click shield.

    AD7124                  | mikroBUS™ | Raspberry Pi
    Name              Pin   | Pin Name  | Pin  Notes
    ---------------------------------------------------------
                      NC    | 1   AN    |  7   GPIO4
                            |           | 33   GPIO13
    Synchronization   SYN   | 2   RST   | 29   GPIO5
                            |           | 35   GPIO19
    SPI Chip Select   CS    | 3   CS    | 24   GPIO8/CS0
                            |           | 26   GPIO7/CS1
    SPI Clock         SCK   | 4   SCK   | 23   GPIO11/SPI-SCK
    SPI Data Out/RDY  SDO   | 5   MISO  | 21   GPIO9/SPI-MISO
    SPI Data In       SDI   | 6   MOSI  | 19   GPIO10/SPI-MOSI
    Power supply      +3.3V | 7   +3.3V | 1,17 +3.3V
    Ground            GND   | 8   GND   | 6,9,14,20,25,30,34,39 GND

NOTES

1. Only pins 1 to 8 of the mikroBus are used, the others are all not 
connected so are not shown.
1. The Pi2 click shield has two positions for the ADC.  Most connections 
to the Raspberry Pi are shared but 3 are not.  Where there are two 
entries for a mikroBus pin, the top one is position 1.
1. Max SPI speed is limited by the SCK high and low pulse times, 100ns 
for each (datasheet t3 and t4 times), so 200ns per cycle = 5MHz.

## Development 

I started out trying to use the Python package spidev but it is poorly
documented and does not do what I expected it to do.  So I decided to
switch over to pigpio instead as I know this works.

## Analog Devices Source Code

https://wiki.analog.com/resources/tools-software/uc-drivers/ad7124

Source code ferom here:
https://github.com/analogdevicesinc/no-OS/tree/master/drivers/adc/ad7124

### SPI header file

This needs to be implemented.

There are three functions which are called by the AD7124 driver:

SPI_Init() – initializes the communication peripheral.
SPI_Write() – writes data to the device.
SPI_Read() – reads data from the device.

