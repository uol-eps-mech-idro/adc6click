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
        """ Set default values for the given channel number.
        Channel 0 uses pin 0 and setup 0.
        Channel 1 uses pin 1 and setup 1.
        FIXME: This is a bit of a hack as only 2 channels are supported.
        """
        if number == 0:
            self._setup = 0
            self._positive_pin = 0  # AIN0
            self._negative_pin = 0b1001  # Ground
            self._enabled = True
            self._scale = 1.0
        elif number == 1:
            self._setup = 1
            self._positive_pin = 1  # AIN1
            self._negative_pin = 0b1001  # Ground
            self._enabled = True
            self._scale = 1.0
        # else:
            # raise ValueError("number out of range")

    @property
    def number(self):
        return self._number

    def write(self, pi, spi):
        """ Write the internal values to the various ADC registers. """
        # The value contains 16 bits.
        value = 0
        ainm = self._negative_pin & 0x1f
        value |= ainm  # bits 4:0
        ainp = self._positive_pin & 0x1f
        value |= (ainp << 5)  # bits 9:5
        setup = self._setup & 0x07
        value |= (setup << 12)  # bits 14:12
        enabled = self._enabled & 0x01
        value |= (enabled << 15)  # bit 15
        # Set channel register.
        register_enum = AD7124RegNames(
                AD7124RegNames.CH0_MAP_REG.value + self._number)
        print("channel.write: enum:", register_enum, "value:", value)
        spi.write_register(pi, register_enum, value)

    def read(self, pi, spi):
        """ Return the voltage of the channel after scaling. """
        result = spi.read_register(pi, AD7124RegNames.DATA_REG)
        int_value = (result[0] << 16) + (result[1] << 8) + result[2]
        value = int_value * self._scale
        print("channel.read:", result, int_value, value)
        return value
