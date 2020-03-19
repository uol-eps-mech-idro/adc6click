#!/usr/bin/env python3
""" Hides the SPI calls from the driver.
Uses PiGPIO for SPI and GPIO access. http://abyz.me.uk/rpi/pigpio/
The PiGPIO daemon must be running before using this script.  Start
using::
    sudo pigpiod
"""

import pigpio


def bytes_to_string(data):
    return [hex(i) for i in data]


class AD7124SPI:
    """ A wrapper that hides the SPI calls from the driver.
    """

    # Values for SPI communications.  All other values are default.
    # Max SPI baud rate is 5MHz.
    AD7124_SPI_BAUD_RATE = 5 * 1000 * 1000
    # AD7124_SPI_BAUD_RATE = 32 * 1000 # for debugging only.
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
            raise ValueError("ERROR: position must be 1 or 2")
        # print("init: channel", spi_channel)
        # Open SPI device
        self._spi_handle = self._pi.spi_open(
            spi_channel, self.AD7124_SPI_BAUD_RATE, spi_flags
        )

    def __del__(self):
        """ Tidy up before being destroyed. """
        self._pi.stop()

    def read_register(self, to_send):
        """ Performs a SPI read using the to_send data.
        :param to_send: The bytes to send.
        :returns: Tuple containing (count of bytes read, data as bytes).
        """
        # print("read_register: to_send:", bytes_to_string(to_send))
        (count, data) = self._pi.spi_xfer(self._spi_handle, to_send)
        # print("read_register: count:", count, "data:", bytes_to_string(data))
        return (count, data)

    def write_register(self, to_send):
        """ The bytes in to_send is wrtten to the SPI bus.
        :param to_send: The bytes to send.
        """
        # print("write_register:", bytes_to_string(to_send))
        self._pi.spi_write(self._spi_handle, to_send)
