#!/usr/bin/env python3
""" Hides the SPI calls from the driver.
"""

import pigpio
import time

from ad7124registers import AD7124RegNames, AD7124Registers


class AD7124SPI:
    """ A wrapper that hides the SPI calls.
    """
    # Values for SPI communications.  All other values are default.
    # Max SPI baud rate is 5MHz.
    # AD7124_SPI_BAUD_RATE = 5 * 1000 * 1000
    AD7124_SPI_BAUD_RATE = 32 * 1000
    AD7124_SPI_MODE = 0b00  # Mode 3

    def __init__(self):
        """ Initialises the AD7124 device. """
        self._pi = pigpio.pi()
        self._registers = AD7124Registers()
        self._spi_handle = 0

    def init(self, pi, position):
        """ Initialises the AD7124..
        position is the Pi2 click shield position number, 1 or 2.
        Throws an exception if it fails.
        """
        # print("init")
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
        self._spi_handle = pi.spi_open(spi_channel, self.AD7124_SPI_BAUD_RATE,
                                       spi_flags)
        # print("init 2")
        self._reset(pi)
        # Check correct device is present.
        ad7124_id = self._read_id(pi)
        # print("init id", ad7124_id)
        if ad7124_id not in (0x14, 0x16):
            raise OSError('ERROR: device on SPI bus is NOT an AD7124!')

    def term(self, pi):
        """ Terminates the AD7124. """
        # print("term: pi", pi)
        pi.spi_close(self._spi_handle)

    def _reset(self, pi):
        """ Resets the AD7124 to power up conditions. """
        to_send = b'\xff\xff\xff\xff\xff\xff\xff\xff'
        # print("reset command", to_send)
        pi.spi_xfer(self._spi_handle, to_send)
        # TODO WAIT UNTIL PROPERLY READY
        time.sleep(0.001)

    def _read_id(self, pi):
        """ The value of the ID register is returned. """
        result = 0
        # print("read_id")
        to_send = []
        command = self._build_command(AD7124RegNames.ID_REG, True)
        to_send.append(command)
        to_send.append(0)
        (count, data) = pi.spi_xfer(self._spi_handle, to_send)
        # print("read_id", count, data)
        # Value is in second byte.
        if count == 2:
            result = data[1]
        return result

    def _build_command(self, register_enum, read=False):
        """ Builds a command byte.
        First bit (bit 7) must be a 0.
        Second bit (bit 6) is read (1) or write (0).
        Remaining 6 bits are register address.
        """
        command = 0
        if read:
            command += (1 << 6)
        command += (register_enum.value & 0x3f)
        return command

    def write_register(self, pi, register_enum, value):
        """ Write the given value to the given register.
        """
        # Command value
        to_send = []
        command = self._build_command(register_enum)
        to_send.append(command)
        # Convert value to bytes.
        num_bytes = self._registers.size(register_enum)
        value_bytes = value.to_bytes(num_bytes, byteorder='big')
        to_send += value_bytes
        # Print to_send as hex values for easier debugging.
        to_send_string = [hex(i) for i in to_send]
        print("write_register: to_send", to_send_string)
        # Write the data.
        pi.spi_xfer(self._spi_handle, to_send)

    def read_register(self, pi, register_enum):
        """ Returns the value read from the register as a list of int values.
        """
        to_send = []
        command = self._build_command(register_enum, True)
        to_send.append(command)
        # Send correct number of padding bytes to get result.
        size = self._registers.size(register_enum)
        num_bytes = self._registers.size(register_enum)
        value = 0
        value_bytes = value.to_bytes(num_bytes, byteorder='big')
        to_send += value_bytes
        (count, data) = pi.spi_xfer(self._spi_handle, to_send)
        # print("read_register: count", count, "data", data)
        value = 0
        if count == size + 1:
            # Remove first byte as always 0xFF
            data = data[1:]
            for byte_value in data:
                value = value << 8
                value |= byte_value
        #print("read_register: value", hex(value))
        return value
