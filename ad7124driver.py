#!/usr/bin/env python3
""" AD7124-8 driver using the Mikro ADC6Click board on the Raspberry Pi.
Uses PiGPIO for SPI and GPIO access. http://abyz.me.uk/rpi/pigpio/

Please install the following packages before first use.
TODO

Before running this script, the pigpio daemon must be running.
 sudo pigpiod

"""

import pigpio

class AD7124Driver:
    """ Provides a wrapper that hides the SPI calls and many of the
    messy parts of the AD7124 implementation.
    """
    # Values for SPI communications.  All other values are default.
    # Max SPI baud rate is 5MHz. 
    # AD7124_SPI_BAUD_RATE = 5 * 1000 * 1000
    AD7124_SPI_BAUD_RATE = 32 * 1000
    AD7124_SPI_MODE = 0b11  # Mode 3

    def __init__(self):
        """ Initialises the AD7124 device. """
        self._pi = None
        self._spi_handle = None

    def init(self, position):
        """ Initialises the AD7124..
        position is the Pi2 click shield position number, 1 or 2.
        Throws an exception if it fails.
        """
        print("init")
        # Set to mode 3
        spi_flags = 0
        spi_flags |= self.AD7124_SPI_MODE
        # Convert position to bus
        spi_bus = 0
        if position == 1:
            spi_bus = 0  # CS0
        elif position == 2: 
            # Only supported on model 2 and later.
            self.__hw_version = self._pi.get_hardware_revision()
            if self.__hw_version >= 2:
                spi_bus = 1  # CS1
            else:
                raise ValueError("position 2 not supported for this board")
        else:
            raise ValueError('ERROR: position must be 1 or 2')
        # Open SPI device
        self._pi = pigpio.pi()
        print("init 1")
        self._spi_handle = self._pi.spi_open(spi_bus, self.AD7124_SPI_BAUD_RATE, spi_flags)
        print("init 2")

    def term(self):
        """ Terminates the AD7124. """
        print("term")
        self._pi.spi_close(self._spi_handle)
        self._pi.stop()

    def read_register(self, register):
        """ The value of the given register is returned.
        """
        print("read_register")
        if register < 0 and register > 0x38:
            raise ValueError("ERROR: register must be in range 0 to 56 inclusive")
        # Add range check of register. Exception if out of range. 
        # 
        # HACK Read ID reg.
        #define AD7124_ID_REG        0x05
        to_send = [0x05, 0]
        (count, data) = self._pi.spi_xfer(self._spi_handle, to_send)
        if count < 0:
            data = []
        return data
        
        result = self.spi.xfer(to_send)
        print("read_register result", result)
        return result

    def reset(self):
        """ Resets the AD7124 to power up conditions. """
        pass

    def write_register(self, register, data):
        """ The data is wrtten to the given register.
        Return True if the value was successfully written.
        """
        result = False
        return result

