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

    def __init__(self, number, pin, setup_num, scale, unipolar=False, bipolar=False,
                 temperature=False):
        """ Set values for the given channel number.
        Note: only single pin inputs are used.
        """
        if not 0 <= number <= 15:
            raise ValueError("channel number" + str(number) + " out of range")
        self._number = number
        if not 0 <= setup_num <= 7:
            raise ValueError("channel setup" + str(setup) + " out of range")
        self._setup_num = setup_num
        if not 0 <= pin <= 15:
            raise ValueError("channel pin" + str(number) + " out of range")
        self._positive_pin = pin
        self._negative_pin = 0b1001  # Ground
        self._enabled = True
        self._scale = scale
        self._unipolar = unipolar
        self._bipolar = bipolar
        self._temperature = temperature

    @property
    def number(self):
        return self._number

    def set(self, pi, spi):
        """ Write the internal values to the various ADC registers. """
        # The value contains 16 bits.
        value = 0
        ainm = self._negative_pin & 0x1f
        value |= ainm  # bits 4:0
        ainp = self._positive_pin & 0x1f
        value |= (ainp << 5)  # bits 9:5
        setup = self._setup_num & 0x07
        value |= (setup << 12)  # bits 14:12
        enabled = self._enabled & 0x01
        value |= (enabled << 15)  # bit 15
        # Set channel register.
        register_enum = AD7124RegNames(
                AD7124RegNames.CH0_MAP_REG.value + self._number)
        # print("channel.write: enum:", register_enum, "value:", bin(value))
        spi.write_register(pi, register_enum, value)

    def get(self, pi, spi):
        """ Gets the value of the channel control register.
        Returns integer.
        """
        # Set channel register.
        register_enum = AD7124RegNames(
                AD7124RegNames.CH0_MAP_REG.value + self._number)
        # Read the register.
        result = self._spi.read_register(self._pi, register_enum)
        return result

    def _to_bipolar_volts(self, int_value):
        volts = 0.0
        int_value -= 0x800000
        volts = int_value * self._scale
        # print("channel.read: V", hex(int_value), value)
        return volts

    def _to_unipolar_volts(self, int_value):
        volts = 0.0
        volts = int_value * self._scale
        # print("channel.read: V", hex(int_value), value)
        return volts

    def _to_temperature(self, int_value):
        """ Convert ADC value to temperature in degrees Celcius.
        """
        temperature_c = 0.0
        int_value -= 0x800000
        # print("channel.read: B", hex(int_value))
        temperature_c = float(int_value)
        temperature_c /= 13584
        # print("channel.read: C", value)
        temperature_c -= 272.5
        # print("channel.read: D", value)
        return temperature_c

    def interpret(self, int_value):
        """ Return the voltage/temperature after scaling. """
        if self._unipolar:
            value = self._to_bipolar_volts(int_value)
        elif self._bipolar:
            value = self._to_unipolar_volts(int_value)
        elif self._temperature:
            value = self._to_temperature(int_value)
        return value
