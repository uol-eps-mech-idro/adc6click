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

    def __init__(self, number):
        self._number = number
        self._bipolar = False
        self._differential = False

    def set_bipolar(self, bipolar):
        self._bipolar = bipolar

    def set_single(self, pin):
        self._differential = False

    def set_differential(self, pin1, pin2):
        self._differential = True

    def setup0_hack(self):
        """ Returns the values for each of the four registers. """
        settings = []
        # default: value = 0x0860
        # 15:12  Always 0
        # 11     bipolar off 0 (default is on)
        # 10:9   burnout current, 0 = off.
        # 8:5    buffer bits. Default is 5 = 1, 6 = 1
        # 4:3    REF_SEL. Default is 0, REFIN1+/REFIN1-
        # 2:0    PGA gain - 0 for now.
        value = 0x0060
        register_enum = AD7124RegNames.CFG0_REG
        configuration_reg = (register_enum, value)
        print("configuration_reg", configuration_reg)
        settings.append(configuration_reg)
        value = 0x060180
        filter_reg = (AD7124RegNames.FILT0_REG, value)
        settings.append(filter_reg)
        value = 0x800000
        offset_reg = (AD7124RegNames.OFFS0_REG, value)
        settings.append(offset_reg)
        # Leave this as set to 1 on power up.
        # value = 0x
        # gain_reg = (AD7124RegNames.GAIN0_REG, value)
        # settings.append(gain_reg)
        return settings

    def write(self, pi, spi):
        """ Write the internal values to the various ADC registers. """
        settings = self.setup0_hack()
        for setting in settings:
            register_enum = setting[0]
            value = setting[1]
            print("setup.write: enum", register_enum.name,
                  "enum value", register_enum.value, "value", value)
            # Write the data
            spi.write_register(pi, register_enum, value)
