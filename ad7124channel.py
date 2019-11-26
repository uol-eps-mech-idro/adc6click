""" Implements a channel class for the AD7124 driver.
"""

from ad7124setup import AD7124Setup
from ad7124spi import AD7124SPI

class AD7124Channel:
    """ This class represents the channel concept of the AD7124.
    Each AD7124 "channel" has:
        An input pin (may be internal).
        A link to a shared "setup".
    This class is simplifies the setup needed for basic operation by setting
    defaults that do what is generally needed.
    """

    def __init__(self, spi, number):
        self._spi = spi;
        self._number = number;
        self._setup = None
        self._pin = 0

    def set_defaults(self):
        """ Set the channel to use bipolar inputs and setup[0].
        """
        pass
    
    def set_input_pin(self, pin):
        self._pin = pin
        
    def use_setup(self, setup):
        self._setup = setup

    def write(self):
        """ Write the internal values to the various ADC registers. """
        # self._spi.write_register(register, value)
        pass

    @property
    def number(self):
        return self._number

    def read(self):
        value = 0.0
        result = self._spi.read_no_wait()
        # TODO Convert result into value.
        return value

