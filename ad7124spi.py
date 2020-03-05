#!/usr/bin/env python3
""" Hides the SPI calls from the driver.
"""

import pigpio


class AD7124SPI:
    """ A wrapper that hides the SPI calls.
    """
    # Values for SPI communications.  All other values are default.
    # Max SPI baud rate is 5MHz.
    AD7124_SPI_BAUD_RATE = 5 * 1000 * 1000
    # AD7124_SPI_BAUD_RATE = 32 * 1000
    AD7124_SPI_MODE = 0b00  # Mode 3

    def __init__(self):
        """ Initialises the AD7124 device. """
        self._pi = pigpio.pi()
        self._spi_handle = 0

    def init(self, position):
        """ Initialises the AD7124.
        Throws an exception if it fails.
        :param position: The position
        :type position: integer
        """
        print("\ninit: baud rate:", self.AD7124_SPI_BAUD_RATE)
        # The Pi2 click shield only supports main bus, bit 8 = 0.
        spi_flags = 0
        # Set to mode 3
        spi_flags |= self.AD7124_SPI_MODE
        # print("init: flags", spi_flags)
        # Set SPI chip select
        spi_channel = 0
        if position in (1, 2):
            spi_channel = position - 1
        else:
            raise ValueError('ERROR: position must be 1 or 2')
        # print("init: channel", spi_channel)
        # Open SPI device
        self._spi_handle = self._pi.spi_open(spi_channel,
                                             self.AD7124_SPI_BAUD_RATE,
                                             spi_flags)

    def term(self):
        """ Terminates the AD7124. """
        # print("term: pi", pi)
        self._pi.spi_close(self._spi_handle)

    def read_register(self, to_send):
        """ Gets data from the a register.
        :param to_send: The command with the correct number of padding bytes to
            receive the data.
        :type to_send: bytes
        :returns: The value read from the register as a tuple of
            (count, list of bytes).
        :rtype: tuple
        """
        result = self._pi.spi_xfer(self._spi_handle, to_send)
        # print("_read_register: count", result[0], "data", result[1])
        return result

    def write_register(self, to_send):
        """ Write the given value to the given register.
        :param to_send: The command to send.
        :type to_send: bytes
        """
        # Write the data.
        self._pi.spi_xfer(self._spi_handle, to_send)
