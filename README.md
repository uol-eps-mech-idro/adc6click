# ADC6Click

This project implements a Python 3 driver for the MikroElectronica ADC 6 Click
board that uses the AD7214-8 24 bit ADC on a Raspberry Pi.

## The files

The Python driver code is located in the same directory as this file.  The AD7124-8 driver is made up of three files:

1. `ad7124spi.py` Wrapper around the PiGPIO SPI functions.
1. `ad7124registers.py` Enums and parameters for all of the ADC registers.
1. `ad7124driver.py` The driver API.

There is one application, `voltmeter.py`.  This application is designed to read one or two channels of the ADC for a specific piece of hardware that was being used at the University.

There are also some unit test files.  The unit test files serve two purposes:

1. Testing the driver and SPI interface functions.
1. Show the user how the functions under tetst might be used.

Shell scripts are also provided to run the unit tests.

The subdirectories contain:

* `arduino-code` Sample application code for the Arduino.  This code was the most useful.
* `c-code` Sample code from the manufacturer.  Less useful as it did not show how to configure the registers to make the ADC do soemthing useful.
* `docs` PDFs of the datasheeets used to develop the code.
* `pigpio-test` This directory has some cutdown test programs used when debugging the SPI interface.

Finally, there are the markdown files.  One you are reading now, the other explains some of the design concepts, some of the problems found during development and has various references to websites.

## Status

* Complete voltmeter.py and test.
* Full Python documentation.

## Completed

* Implemented top level application.
* Implemented unit tests.
* Work out what the values from the data register mean and how to make them into something sensible.
* Read the ID register.
* Read the status register.
* Read the data register.
