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
        """ Initialise the AD7124 device. """
        self._pi = pigpio.pi()
        self._spi = AD7124SPI()

    def init(self, position):
        """ Initialises the AD7124..
        position is the Pi2 click shield position number, 1 or 2.
        Throws an exception if it fails.
        """
        self._spi.init(self._pi, position)

    def term(self):
        """ Terminates the AD7124. """
        self._spi.term(self._pi)
        self._pi.stop()

    def reset(self):
        """ Resets the AD7124 to power up conditions. """
        pass

    def read_register(self, register):
        """ The value of the given register is returned.
        """
        print("read_register")
        data = []
        return data
        
        result = self.spi.xfer(to_send)
        print("read_register result", result)
        return result

    def write_register(self, register, data):
        """ The data is wrtten to the given register.
        Return True if the value was successfully written.
        """
        result = False
        return result


class AD7124SPI:
    """ Provides a wrapper that hides the SPI calls.
    """
    # Values for SPI communications.  All other values are default.
    # Max SPI baud rate is 5MHz. 
    # AD7124_SPI_BAUD_RATE = 5 * 1000 * 1000
    AD7124_SPI_BAUD_RATE = 32 * 1000
    AD7124_SPI_MODE = 0b11  # Mode 3

    def __init__(self):
        """ Initialises the AD7124 device. """
        self._pi = pigpio.pi()

    def init(self, pi, position):
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
        self._spi_handle = pi.spi_open(spi_bus, self.AD7124_SPI_BAUD_RATE, spi_flags)
        print("init 2")
        # Check correct device is present.
        AD7124Id = self.read_id(pi)
        if AD7124Id != 0x14 or AD7124Id != 0x16:
            raise OSError('ERROR: device on SPI bus is NOT an AD7124!')

    def term(self, pi):
        """ Terminates the AD7124. """
        print("term")
        self.pi.spi_close(self._spi_handle)
        self.pi.stop()

    def read_id(self, pi):
        """ The value of the ID register is returned. """
        print("read_id")
        AD7124_ID_REG = 0x05
        to_send = [AD7124_ID_REG, 0]
        (count, data) = pi.spi_xfer(self._spi_handle, to_send)
        if count < 0:
            data = []
        print("read_id", count, data)
        return data

    def reset(self):
        """ Resets the AD7124 to power up conditions. """
        pass

    def write_register(self, register, data):
        """ The data is wrtten to the given register.
        Return True if the value was successfully written.
        """
        result = False
        return result

    
