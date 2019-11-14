#!/usr/bin/env python3
""" AD7124-8 driver using the Mikro ADC6Click board on the Raspberry Pi.
Please install the following packages before first use.
'sudo apt-get install python3-spidev python3-dev'

Loosely based on C code from here:
https://github.com/analogdevicesinc/no-OS/tree/master/drivers/adc/ad7124
"""

import spidev

class AD7124Driver:
    """ Provides a wrapper that hides the SPI calls and many of the
    messy parts of the AD7124 implementation.
    """
    # Values for SPI communications.  All other values are default.
    # Max SPI frequency is 5MHz. 
    # AD7124_SPI_MAX_MHZ = 5 * 1000 * 1000
    AD7124_SPI_MAX_MHZ = 5 * 1000
    AD7124_SPI_MODE = 0b11  # Mode 3

    def __init__(self):
        """ Initialises the AD7124 device. """
        self.spi_open()

    def __del__(self):
        """ Close the SPI device. """
        self.spi_close()

    def reset(self):
        """ Resets the AD7124 to power up conditions. """
        pass

    def read_register(self, register):
        """ The value of the given register is returned.
        """
        if register < 0 and register > 0x38:
            raise ValueError("ERROR: register must be in range 0 to 56 inclusive")
        # Add range check of register. Exception if out of range. 
        # 
        # HACK Read ID reg.
        #define AD7124_ID_REG        0x05
        to_send = [0x05, 0, 0]
        result = self.spi.xfer(to_send)
        print("read_register result", result)
        return result

    def write_register(self, register, data):
        """ The data is wrtten to the given register.
        Return True if the value was successfully written.
        """
        result = False
        return result

    def spi_open(self, position=2):
        """ Opens the SPI device.
        position is the Pi2 click shield position number, 1 or 2.
        Throws an exception if it fails.
        """
        print("spi_open")
        self.spi = None
        device = -1
        bus = 0  # Always 0 on the Raspberry Pi
        if position == 1:
            device = 0  # CS0
        elif position == 2: 
            device = 1  # CS1
        else:
            raise ValueError('ERROR: position must be 1 or 2')
        try:
            self.spi = spidev.SpiDev()
            self.spi.open(bus, device)
            self.spi.max_speed_hz = self.AD7124_SPI_MAX_MHZ
            self.spi.mode = self.AD7124_SPI_MODE
        except Exception as e:
            print(e)
            GPIO.cleanup()
            if self.spi:
                self.spi.close()
                self.spi = None
            raise OSError('ERROR: could not open SPI', bus, device)

    def spi_close(self):
        """ Close the SPI device. """
        if self.spi:
            self.spi.close()
            self.spi = None
        print("spi_close")
