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

    def __init__(self, index,
                 bipolar=True, internal_ref=False, gain=0,
                 data_rate=0x180, single_cycle=False):
        """ index is in the range 0 to 7 inclusive.
        data_rate filter data output rate. Range 1 to 2047.
        """
        self._index = index
        self._config = ConfigurationRegister(index, bipolar, internal_ref, gain)
        self._filter = FilterRegister(index, data_rate, single_cycle)
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

    def __init__(self, index, bipolar, internal_ref, gain):
        """
        If not internal ref uses REFIN1(+/-) as these are the only pins that
        can be accessed on the ADC 6 Click board.
        gain is in range 0 to 7. 0 gives range of +/-2.5V.
        """
        self._index = index
        self._default_value = 0x0001
        self._value = 0
        if bipolar:
            self._value |= 0x0800
        if internal_ref:
            self._value |= 0x0010
        self._value |= (gain & 0x07)
        # TODO other bits

    def set(self, pi, spi):
        if self._default_value != self._value:
            register_index = AD7124RegNames.CFG0_REG.value + self._index
            register_enum = AD7124RegNames(register_index)
            spi.write_register(pi, register_enum, self._value)


class FilterRegister:
    """ Represents the filter register. """

    def __init__(self, index, data_rate, single_cycle):
        self._index = index
        self._default_value = 0x060180
        self._value = 0
        self._value |= (data_rate & 0x7ff)
        if single_cycle:
            self._value |= 0x010000
        # TODO other bits

    def set(self, pi, spi):
        if self._default_value != self._value:
            register_index = AD7124RegNames.FILT0_REG.value + self._index
            register_enum = AD7124RegNames(register_index)
            spi.write_register(pi, register_enum, self._value)


class OffsetRegister:
    """ Represents the offset register. """

    def __init__(self, index):
        self._index = index
        self._default_value = 0x800000
        # TODO
        self._value = 0x800000

    def set(self, pi, spi):
        if self._default_value != self._value:
            register_index = AD7124RegNames.OFFS0_REG.value + self._index
            register_enum = AD7124RegNames(register_index)
            spi.write_register(pi, register_enum, self._value)


class GainRegister:
    """ Represents the gain register. """

    def __init__(self, index):
        self._index = index
        self._default_value = 0x500000
        # TODO
        self._value = 0x500000

    def set(self, pi, spi):
        if self._default_value != self._value:
            register_index = AD7124RegNames.GAIN0_REG.value + self._index
            register_enum = AD7124RegNames(register_index)
            spi.write_register(pi, register_enum, self._value)
