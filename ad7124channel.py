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

    def __init__(self, channel):
        """ Set default values for the given channel number.
        Channel 1 uses pin 1 and setup 1.
        Channel 2 uses pin 2 and setup 2.
        TODO Add parameters?
        """
        # Defaults to do nothing
        self._channel = channel
        self._setup = 0
        self._positive_pin = 0b1001  # Ground
        self._negative_pin = 0b1001  # Ground
        self._enabled = False
        self._scale = 1.0
        if 0 <= channel <= 15:
            # Configure each channel here.
            if channel == 1:
                self._setup = 1
                self._positive_pin = 1  # AIN1
                # self._enabled = False
                self._enabled = True
            elif channel == 2:
                self._setup = 2
                self._positive_pin = 2  # AIN2
                # self._enabled = False
                self._enabled = True
            elif channel == 15:
                self._setup = 7  # Use default setup
                self._positive_pin = 0b1000  # Temperature
                self._negative_pin = 0b1000  # Temperature
                self._enabled = True
                self._scale = 0.0
        else:
            raise ValueError("channel " + str(channel) + " out of range")

    @property
    def channel(self):
        return self._channel

    def set(self, pi, spi):
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
                AD7124RegNames.CH0_MAP_REG.value + self._channel)
        # print("channel.write: enum:", register_enum, "value:", bin(value))
        spi.write_register(pi, register_enum, value)

    def read(self, pi, spi):
        """ Return the voltage of the channel after scaling. """
        value = 0.0
        int_value = spi.read_register(pi, AD7124RegNames.DATA_REG)
        # print("channel.read: A", hex(int_value))
        if self._scale == 0.0:
            int_value -= 0x800000
            # print("channel.read: B", hex(int_value))
            value = float(int_value)
            value /= 13584
            # print("channel.read: C", value)
            value -= 272.5
            # print("channel.read: D", value)
        else:
            value = int_value * self._scale
            # print("channel.read: V", int_value, value)
        return value

