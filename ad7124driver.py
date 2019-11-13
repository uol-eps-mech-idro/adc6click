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
        to_send = [0x01, 0x02, 0x03]
        result = self.spi.xfer(to_send)
        return result

    def write_register(self, register, data):
        """ The data is wrtten to the given register.
        Return True if the value was successfully written.
        """
        result = False
        return result

    def spi_open(self, position=1):
        """ Opens the SPI device.
        position is the Pi2 click shield position number, 1 or 2.
        Returns None if it fails.
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
            self.spi.max_speed_hz = 10000000  # FIXME
            self.spi.mode = 0b00  # FIXME
            self.spi.lsbfirst = False  # FIXME
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
