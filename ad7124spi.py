#!/usr/bin/env python3
""" Hides the SPI calls from the driver.
"""

import pigpio

from ad7124registers import AD7124Registers
from ad7124registers import AD7124RegNames

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

    def init(self, pi, position): # pylint: disable=C0103
        """ Initialises the AD7124..
        position is the Pi2 click shield position number, 1 or 2.
        Throws an exception if it fails.
        """
        print("init")
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
        self._spi_handle = pi.spi_open(spi_channel, self.AD7124_SPI_BAUD_RATE, spi_flags)
        # print("init 2")
        # Check correct device is present.
        ad7124_id = self._read_id(pi)
        # print("init id", ad7124_id)
        if ad7124_id not in (0x14, 0x16):
            raise OSError('ERROR: device on SPI bus is NOT an AD7124!')

    def term(self, pi): # pylint: disable=C0103
        """ Terminates the AD7124. """
        print("term")
        pi.spi_close(self._spi_handle)

    def _read_id(self, pi): # pylint: disable=C0103
        """ The value of the ID register is returned. """
        result = 0
        # print("read_id")
        to_send = []
        # Build command word
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
        """ Builds a command byte. """
        command = 0
        # First bit (bit 7) must be a 0
        # Second bit (bit 6) is read (1) or write (0).
        if read:
            command += (1 << 6)
        # Remaining 6 bits are register address.
        command += (register_enum.value & 0x2f)
        return command

    def write_register(self, pi, register_enum, data): # pylint: disable=C0103
        """ Write the given data to the given register.
        """
        if len(data) == self._registers.size(register_enum):
            to_send = []
            register_address = register_enum.value
            command = self._build_command(register_address)
            to_send.append(command)
            to_send += data
            print("_write_register: to_send", to_send)
            pi.spi_xfer(self._spi_handle, to_send)
        else:
            raise ValueError("Length of data does not match the size of the register.")

    def read_register(self, pi, register_enum): # pylint: disable=C0103
        """ Returns the value read from the register as a list of int values.
        """
        address = register_enum
        size = self._registers.size(register_enum)
        to_send = []
        command = self._build_command(address, True)
        to_send.append(command)
        for _ in range(0, size):
            to_send.append(0)
        (count, data) = pi.spi_xfer(self._spi_handle, to_send)
        if count == size + 1:
            # Remove first value as always 0xFF
            data = data[1:]
        else:
            data = []
        return data

    def reset(self, pi): # pylint: disable=C0103
        """ Resets the AD7124 to power up conditions. """
        to_send = b'\xff\xff\xff\xff\xff\xff\xff\xff'
        print("reset command", to_send)
        pi.spi_xfer(self._spi_handle, to_send)
        # TODO WAIT UNTIL DONE

    def read_status(self, pi): # pylint: disable=C0103
        """ Returns a tuple containing the values:
        (ready {bool}, error{bool}, power on reset{bool}, active channel)
        """
        # RDY is inverted.
        ready = True
        error = False
        power_on_reset = False
        active_channel = 0
        data = self.read_register(pi, AD7124RegNames.STATUS_REG)
        print("read_status", data)
        # FIXME Is this right?  Should be only one byte?
        if len(data) == 2:
            value = data[1]
            if value & 0x80:
                ready = False
            if value & 0x40:
                ready = True
            if error & 0x10:
                power_on_reset = True
            active_channel &= 0x0f
        return (ready, error, power_on_reset, active_channel)

    def write_reg_control(self, pi, power_mode=0, mode=0, clock_select=0): # pylint: disable=C0103
        """ Writes to the ADC control register.
        Default value of the register is 0x00 so defaults of 0 work.
        """
        to_send = []
        # The control register is 16 bits, MSB first.
        # MSB - for now all 0s.
        msb = 0b00000000
        to_send.append(msb)
        # Pack the given parameters
        lsb = clock_select
        lsb |= ((mode & 0x0f) << 2)
        lsb |= ((power_mode & 0x03) << 6)
        to_send.append(lsb)
        print("_write_reg_control to_send", to_send)
        self.write_register(pi, AD7124RegNames.ADC_CTRL_REG, to_send)
