""" Implements a setup class for the AD7124 driver.
"""

from ad7124spi import AD7124SPI
from ad7124registers import AD7124RegNames


class AD7124Setup:
    """ This class represents the setup concept of the AD7124.
    Each AD7124 setup has:

    This class is simplifies the setup needed for basic operation by setting
    defaults that do what is generally needed and only providing additional
    functions to set values that can be changed.

    Each setup is made up of four registers: configuration, filter, gain and
    offset.  Most of the registers do not need to be setup.
    """

    def __init__(self, index):
        """ index is in the range 0 to 7 inclusive. """
        self._index = index
        self._config = ConfigurationRegister(index)
        self._filter = FilterRegister(index)
        self._offset = OffsetRegister(index)
        self._gain = GainRegister(index)

    def set(self, pi, spi):
        """ Write the internal values to the various ADC registers. """
        self._config.set(pi, spi)
        self._filter.set(pi, spi)
        self._offset.set(pi, spi)
        self._gain.set(pi, spi)


class ConfigurationRegister:
    """ Represents the configuration register. """

    def __init__(self, index):
        self._index = index
        # Use defaults
        self._value = 0x0860
        # FIXME hack
        if index == 1:
            # Bipolar, use internal ref. voltage 0b10
            # All buffer bits set, PGA = 0 (gain of 1)
            self._value = 0x09f0

    def set(self, pi, spi):
        register_index = AD7124RegNames.CFG0_REG.value + self._index
        register_enum = AD7124RegNames(register_index)
        spi.write_register(pi, register_enum, self._value)


class FilterRegister:
    """ Represents the filter register. """

    def __init__(self, index):
        self._index = index
        # Use defaults
        self._value = 0x060180

    def set(self, pi, spi):
        register_index = AD7124RegNames.FILT0_REG.value + self._index
        register_enum = AD7124RegNames(register_index)
        spi.write_register(pi, register_enum, self._value)


class OffsetRegister:
    """ Represents the offset register. """

    def __init__(self, index):
        self._index = index
        # Use defaults
        self._value = 0x800000

    def set(self, pi, spi):
        register_index = AD7124RegNames.OFFS0_REG.value + self._index
        register_enum = AD7124RegNames(register_index)
        spi.write_register(pi, register_enum, self._value)


class GainRegister:
    """ Represents the gain register. """

    def __init__(self, index):
        self._index = index
        # Use defaults
        self._value = 0x500000

    def set(self, pi, spi):
        register_index = AD7124RegNames.GAIN0_REG.value + self._index
        register_enum = AD7124RegNames(register_index)
        spi.write_register(pi, register_enum, self._value)
