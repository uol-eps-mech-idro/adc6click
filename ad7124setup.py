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

    def __init__(self, number):
        self._number = number;
        self._bipolar = False
        self._differential = False

    def set_bipolar(self, bipolar):
        self._bipolar = bipolar

    def set_single(self, pin):
        self._differential = False

    def set_differential(self, pin1, pin2):
        self._differential = True

    def write(self, pi, spi):
        """ Writes all internal settings to the various registers.
        """
        pass
