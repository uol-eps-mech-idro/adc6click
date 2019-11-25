#!/usr/bin/env python3
""" Hides the SPI calls from the driver.
"""

import time
import pigpio
import bitstruct

class AD7124SPI:
    """ A wrapper that hides the SPI calls.
    """
    # Values for SPI communications.  All other values are default.
    # Max SPI baud rate is 5MHz. 
    # AD7124_SPI_BAUD_RATE = 5 * 1000 * 1000
    AD7124_SPI_BAUD_RATE = 32 * 1000
    AD7124_SPI_MODE = 0b00  # Mode 3
    AD7124_REG_CONTROL = 0x01
    AD7124_REG_ID = 0x05
    

    def __init__(self):
        """ Initialises the AD7124 device. """
        self._pi = pigpio.pi()

    def init(self, pi, position):
        """ Initialises the AD7124..
        position is the Pi2 click shield position number, 1 or 2.
        Throws an exception if it fails.
        """
        print("init")
        # The Pi2 click shield only supports main bus, bit 8 = 0.
        spi_flags = 0
        # Set to mode 3
        spi_flags |= self.AD7124_SPI_MODE
        print("init: flags", spi_flags)
        # Set SPI chip select
        spi_channel = 0
        if position == 1 or position == 2: 
            spi_channel = position - 1
        else:
            raise ValueError('ERROR: position must be 1 or 2')
        print("init: channel", spi_channel)
        # Open SPI device
        self._spi_handle = pi.spi_open(spi_channel, self.AD7124_SPI_BAUD_RATE, spi_flags)
        print("init 2")
        # Check correct device is present.
        AD7124Id = self.read_id(pi)
        print("init id", AD7124Id)
        if AD7124Id != 0x14 and AD7124Id != 0x16:
            raise OSError('ERROR: device on SPI bus is NOT an AD7124!')

    def term(self, pi):
        """ Terminates the AD7124. """
        print("term")
        pi.spi_close(self._spi_handle)

    def read_id(self, pi):
        """ The value of the ID register is returned. """
        result = 0
        # print("read_id")
        to_send = []
        # Build command word
        command = self._build_command_word(self.AD7124_REG_ID, True)
        to_send.append(command)
        to_send.append(0)
        (count, data) = pi.spi_xfer(self._spi_handle, to_send)
        # print("read_id", count, data)
        # Value is in second byte.
        if count == 2:
            result = data[1]
        return result

    def _build_command_word(self, register, read = False):
        """ Builds a command value to be sent to the communications register. """
        command = 0
        # First bit (bit 7) must be a 0
        # Second bit (bit 6) is read (1) or write (0).
        if read:
            command += (1 << 6)
        # Remaining 6 bits are register value.
        command += (register & 0x2f)
        return command

    def read_reg_1(self, pi):
        """ Does a single shot conversion. 
        The value of the ??? register is returned. 
        """
        # Set single shot coversion mode.
        self._write_reg_control(pi, mode=0x01)
        # Wait for conversion - fastest is @ 19200Hz or 52uS.
        # 100uS is fine.
        time.sleep(0.0001)
        # Command 0x42 plus three bytes for the result.
        read_command = [0x42, 0, 0, 0]
        (count, data) = pi.spi_xfer(self._spi_handle, read_command)
        if count < 0:
            data = []
        print("read_reg_1", count, data)
        
        return data

    def _write_reg_control(self, pi, power_mode=0, mode=0, clock_select=0):
        """ Writes to the ADC control register.
        Default value of the register is 0x00 so parameter defaults of 0 work.
        """
        command = [self.AD7124_REG_CONTROL, 0]
        value = bitstruct.compile('u2u4u2')
        value_bytes = value.pack(power_mode, mode, clock_select)
        #print("_write_reg_control bytes", value_bytes)
        value_ints = bitstruct.unpack('u8', value_bytes)
        #print("_write_reg_control ints", value_ints)
        command.append(value_ints[0])
        print("_write_reg_control command", command)
        (count, data) = pi.spi_xfer(self._spi_handle, command)
        #print("_write_reg_control result", count, data)

    def reset(self):
        """ Resets the AD7124 to power up conditions. """
        pass

    def write_register(self, register, data):
        """ The data is wrtten to the given register.
        Return True if the value was successfully written.
        """
        result = False
        return result

    
