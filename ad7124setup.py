""" Implements a setup class for the AD7124 driver.
"""

from ad7124spi import AD7124SPI

class AD7124Setup:
    """ This class represents the setup concept of the AD7124.
    Each AD7124 setup has:

    This class is simplifies the setup needed for basic operation by setting
    defaults that do what is generally needed and only providing additional 
    functions to set values that can be changed.
    """

    def __init__(self, spi, number):
        self._spi = spi;
        self._number = number;
        self._bipolar = False

    def set_defaults(self):
        """ Configure the setup to use:
        TODO
        """

    # This is a setter so conver to property.
    def set_bipolar_input(self, bipolar):
        self._bipolar = bipolar

    def write(self):
        """ Writes all internal settings to the various registers.
        """
        pass
