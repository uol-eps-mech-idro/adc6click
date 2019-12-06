#!/usr/bin/env python3
""" AD7124-8 driver using the Mikro ADC6Click board on the Raspberry Pi.
Uses PiGPIO for SPI and GPIO access. http://abyz.me.uk/rpi/pigpio/

Please install the following packages before first use.
TODO


Before running this script, the pigpio daemon must be running.
 sudo pigpiod

"""
import time
import pigpio
from ad7124spi import AD7124SPI
from ad7124channel import AD7124Channel
from ad7124setup import AD7124Setup
from ad7124registers import AD7124RegNames


class AD7124Driver:
    """ Provides a wrapper that hides the SPI calls and many of the
    messy parts of the AD7124 implementation.
    """

    def __init__(self):
        """ Initialise the AD7124 device. """
        self._pi = pigpio.pi()
        self._spi = AD7124SPI()
        self._setups = []
        self._channels = []

    def init(self, position):
        """ Initialises the AD7124..
        position is the Pi2 click shield position number, 1 or 2.
        Throws an exception if it fails.
        """
        self._spi.init(self._pi, position)
        for i in range(0, 16):
            channel = AD7124Channel(i)
            self._channels.append(channel)
        for i in range(0, 8):
            setup = AD7124Setup(i)
            self._setups.append(setup)

    def term(self):
        """ Terminates the AD7124. """
        self._spi.term(self._pi)
        self._pi.stop()

    def reset(self):
        """ Resets the AD7124 to power up conditions. """
        self._spi.reset(self._pi)

    def configure(self, channel):
        """ Set up the given channel.
        Must be called after init.
        """
        # FIXME This is a quick hack to get something working.
        # channel is ignored.  Using channel 0 and setup 0.
        # write_register(self, pi, register_enum, data)
        self._setups[0].write(self._pi, self._spi)
        self._channels[0].write(self._pi, self._spi)

    def read_voltage(self, channel_num):
        """ The Voltage of the given channel is returned.
        """
        channel = self._channels[channel_num]
        voltage = channel.read(self._pi, self._spi)
        print("read_voltage: ", voltage)
        return voltage

    def read_register(self, register_name):
        # NOT TESTED
        """ The value of the given register is returned.
        """
        print("read_register")
        result = self._spi.read_register(self._pi, register_name)
        print("read_register result", result)
        return result

    def write_register(self, register, data):
        # FIXME
        """ The data is wrtten to the given register.
        Return True if the value was successfully written.
        """
        result = False
        return result

    def read_channels(self):
        # FIXME
        """ Read all active channels and output the values to stdout.
        Can only be called after configure has been called.
        """
        print("Reading all active channels")
        # Print header
        for channel in self._channels:
            # Work out how to put this in columns.
            print("Channel:", channel.number())
        # Continuously read values from all active channels.
        while True:
            try:
                for channel in self._channels:
                    # Work out how to put this in columns.
                    number = channel.number()
                    value = channel.read()
                    # Work out how to arrange this in columns.
                    print("Ch, val:", number, value)
            except KeyboardInterrupt:
                break
        print("Finished")


