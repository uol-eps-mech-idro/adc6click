# ADC6Click

This project implements a Python 3 driver for the MikroElectronica ADC 6 Click
board that uses the AD7214-8 24 bit ADC on a Raspberry Pi.

## Installation

Connect a monitor, keyboard and mouse to the Raspberry Pi 4.  Ensure that the
Install the code by downloading or cloning this repo onto the Raspberry Pi.  Then install the dependencies using the following commands:

```bash
cd adc6click
sudo python3 setup.py develop
```

More information on PiGPIO can be found here:
<http://abyz.me.uk/rpi/pigpio/>
<https://github.com/guymcswain/pigpio-client/wiki/Install-and-configure-pigpiod>

## The files

In same directory as this file we have:

* `.gitignore`.  Tells Git to ignore the specified files.
* `design.md`.  Notes on the design of the AD7124 driver.
* `implemntation.md`.  Notes on the implementation of the AD7124 driver.
* `pdoc.sh`.  Generates the HTML documentation.  See below for details.
* `README.md`.  This file.
* `unittest.sh`.  Runs the unit tests for the AD7124 driver.
* `test_voltmeter.py`.  Runs `test_voltmeter.py`.
* `voltmeter.py`.  This application is designed to read one or two channels of the ADC for a specific piece of hardware that was being used at the University.

The subdirectories contain:

* `ad7124` The driver code.
    * `ad7124driver.py` The driver API.
    * `ad7124registers.py` Enums and parameters for all of the ADC registers.
    * `ad7124spi.py` Wrapper around the PiGPIO SPI functions.
* `arduino-code` Sample application code for the Arduino.  This code was the most useful.
* `c-code` Sample code from the manufacturer.  Less useful as it did not show how to configure the registers to make the ADC do something useful.
* `docs` PDFs of the datasheets used to develop the code.
* `html` The HTML API documentation for this driver.  Generated using pdoc.
* `pigpio-test` This directory has some cut down test programs used when debugging the SPI interface.
* `test` The unit test files live in here.  Shell scripts are also provided to run the unit tests.  The unit test files serve two purposes:
  1. Testing the driver and SPI interface functions.
  1. Show the user how the functions under test might be used.

## Generating the API documentation

The API of the driver is documented using a mixture of [markdown](
https://github.com/adam-p/markdown-here/wiki/Markdown-Here-Cheatsheet) and
the [Google style docstring](http://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

Generating the HTML documentation must be done on a Raspberry Pi (PiGPIO fails
on a PC).  Make sure you have installed the dependencies (see near top of this
file) and then run:

```bash
./pdoc.sh
```

To view the documentation:

```bash
cd html
firefox index.html
```

## Status

### To Do

* Complete voltmeter.py and test.


### Completed

* Put code onto Raspberry Pi to generate all documentation and commit it.
* Full Python documentation.
* Redo voltage conversion function from first principles.
* Implemented top level application.
* Implemented unit tests.
* Work out what the values from the data register mean and how to make them into something sensible.
* Read the ID register.
* Read the status register.
* Read the data register.
