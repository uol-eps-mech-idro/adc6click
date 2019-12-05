""" Implements a channel class for the AD7124 driver.
"""

from ad7124setup import AD7124Setup
from ad7124spi import AD7124SPI
from ad7124registers import AD7124RegNames

class AD7124Channel:
    """ This class represents the channel concept of the AD7124.
    Each AD7124 "channel" has:
        An input pin (may be internal).
        A link to a shared "setup".
    This class is simplifies the setup needed for basic operation by setting
    defaults that do what is generally needed.
    """

    def __init__(self, number):
        self._setup = None
        self._pin = 0
        # Properties
        self._number = number;
        self._scale = 1.0

    def set_defaults(self):
        """ Set the channel to use bipolar inputs and setup[0].
        """
        pass
    
    def set_input_pin(self, pin):
        self._pin = pin
        
    def use_setup(self, setup):
        self._setup = setup

    @property
    def scale(self):
        return self._scale
        
    @scale.setter
    def scale(self, scale):
        self._scale = scale

    @property
    def number(self):
        return self._number

    def write(self):
        """ Write the internal values to the various ADC registers. """
        # self._spi.write_register(register, value)
        pass

    def read(self, pi, spi):
        """ Return the voltage of the channel after scaling. """
        result = spi.read_register(pi, AD7124RegNames.DATA_REG)
        print("channel.read:", result)
        int_value (result[0] << 16) + (result[1] << 8) + result[2]
        # int_value is in range
        value *= self._scale
        return value

