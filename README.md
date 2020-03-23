# ADC6Click

This project implements a Python 3 driver for the MikroElectronica ADC 6 Click
board that uses the AD7214-8 24 bit ADC on a Raspberry Pi.

## Installation

Install the code by downloading or cloning this repo onto the Raspberry Pi.  Then issue the following commands from the Raspberry Pi command line:

```bash
sudo apt-get update
sudo apt-get install pigpio
```

More information on PiGPIO can be found here:
<http://abyz.me.uk/rpi/pigpio/>
<https://github.com/guymcswain/pigpio-client/wiki/Install-and-configure-pigpiod>

## The files

The Python driver code is located in the same directory as this file.  The AD7124-8 driver is made up of three files:

1. `ad7124spi.py` Wrapper around the PiGPIO SPI functions.
1. `ad7124registers.py` Enums and parameters for all of the ADC registers.
1. `ad7124driver.py` The driver API.

There is one application, `voltmeter.py`.  This application is designed to read one or two channels of the ADC for a specific piece of hardware that was being used at the University.

The subdirectories contain:

* `arduino-code` Sample application code for the Arduino.  This code was the most useful.
* `c-code` Sample code from the manufacturer.  Less useful as it did not show how to configure the registers to make the ADC do soemthing useful.
* `docs` PDFs of the datasheeets used to develop the code.
* `html` The HTML API documentation for this driver.  Generated using pdoc.
* `pigpio-test` This directory has some cutdown test programs used when debugging the SPI interface.
* `test` The unit test files live in here.  Shell scripts are also provided to run the unit tests.  The unit test files serve two purposes:

  1. Testing the driver and SPI interface functions.
  1. Show the user how the functions under tetst might be used.

Finally, there are the markdown files.  One you are reading now, the other explains some of the design concepts, some of the problems found during development and has various references to websites.

## Generating the API documentation

The API of the driver is documented using a mixture of [markdown](
https://github.com/adam-p/markdown-here/wiki/Markdown-Here-Cheatsheet) and
the [Google style docstring](http://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings).

If you want to regenerate the documentation for the module, install pdoc using:

```bash
sudo apt install python3-pip
pip3 install pdoc3
```

Then run:

```bash
~/.local/bin/pdoc3 --html .
```

NOTE: To get the full documentation, you need to have PiGPIO installed so you need to do this on a Raspberry Pi.

## Status

### To Do

* Complete voltmeter.py and test.
* Full Python documentation.
* Put code onto Raspberry Pi to generate all documentation and commit it.

### Completed

* Redo voltage conversion function from first principles.
* Implemented top level application.
* Implemented unit tests.
* Work out what the values from the data register mean and how to make them into something sensible.
* Read the ID register.
* Read the status register.
* Read the data register.
