#!/usr/bin/env python3
""" Hides the SPI calls from the driver.
"""

import pigpio


class AD7124SPI:
    """ A wrapper that hides the SPI calls.
    """
    # Values for SPI communications.  All other values are default.
    # Max SPI baud rate is 5MHz.
    # AD7124_SPI_BAUD_RATE = 5 * 1000 * 1000
    AD7124_SPI_BAUD_RATE = 32 * 1000
    AD7124_SPI_MODE = 0b00  # Mode 3

    def __init__(self, position):
        """ Initialises the AD7124.
        :param position: The Pi2 click shield position number, 1 or 2.
        If the pigpio call fails, error messages are shown on the
        terminal. Throws an exception if position is out of range.
        """
        # print("__init__")
        self._pi = pigpio.pi()
        # The Pi2 click shield only supports main bus, bit 8 = 0.
        spi_flags = 0
        # Set to mode 3
        spi_flags |= self.AD7124_SPI_MODE
        # print("init: flags", spi_flags)
        # Set SPI chip select
        spi_channel = 0
        if position == 1 or position == 2:
            spi_channel = position - 1
        else:
            raise ValueError('ERROR: position must be 1 or 2')
        # print("init: channel", spi_channel)
        # Open SPI device
        self._spi_handle = self._pi.spi_open(
            spi_channel, self.AD7124_SPI_BAUD_RATE, spi_flags)

    def read_register(self, to_send):
        """ Performs a SPI read using the to_send data.
        :param to_send: The bytes to send.
        :returns: The data read by the function.
        """
        to_send_string = [hex(i) for i in to_send]
        print("read_register: to_send:", to_send_string)
        (_, data) = self._pi.spi_xfer(self._spi_handle, to_send)
        data_string = [hex(i) for i in data]
        print("read_register: data:", data_string)
        return data

    def write_register(self, to_send):
        """ The bytes in to_send is wrtten to the SPI bus.
        :param to_send: The bytes to send.
        """
        to_send_string = [hex(i) for i in to_send]
        print("write_register:", to_send_string)
        self._pi.spi_write(self._spi_handle, to_send)
