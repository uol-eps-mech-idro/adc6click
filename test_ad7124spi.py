#!/usr/bin/env python3
""" Unit tests for the AD7124 driver. """
import pigpio
import unittest

from ad7124spi import AD7124SPI
from ad7124registers import AD7124RegNames


class TestAD7214Spi(unittest.TestCase):

    def setUp(self):
        """ Verify init works.
        Can throw an exception if the ADC is not connected.
        """
        self._pi = pigpio.pi()
        self._spi = AD7124SPI()
        position = 1
        self._spi.init(self._pi, position)

    def tearDown(self):
        self._spi.term(self._pi)
        self._pi.stop()

    def test_reset(self):
        """ Reset the AD7124.
        The reset function changes the default for channel 0 to disabled.  This
        proves that it has done the "right thing".
        """
        self._spi.reset(self._pi)
        value = self._spi.read_register(self._pi, AD7124RegNames.CH0_MAP_REG)
        self.assertEqual(0x0001, value)

    def test_read_register(self):
        """ Read the CH1 register.
        Should be 0x0001 after reset command resets default value.
        """
        value = self._spi.read_register(self._pi, AD7124RegNames.CH1_MAP_REG)
        self.assertEqual(0x0001, value)

    def test_read_register_status(self):
        """ Read the CH1 register with status.
        Should be 0x0001 and 0xff.
        """
        result = self._spi.read_register_status(self._pi,
                                                AD7124RegNames.CH1_MAP_REG)
        self.assertEqual(0x0001, result[0])
        self.assertEqual(0xff, result[1])

    def test_write_register(self):
        """ Read, modify and read the CH1 register.
        Read the CH1 register.  Should be 0x0001.
        Then write a new value that changes both bytes.
        Read back to verify change has occurred.
        """
        register = AD7124RegNames.CH1_MAP_REG
        value = self._spi.read_register(self._pi, register)
        self.assertEqual(0x0001, value)
        new_value = 0
        new_value |= (1 << 15)  # 15 Enabled.
        new_value |= (0b10010 << 5)  # 9:5 AINP = Internal reference.
        new_value |= (0b10011)  # 4:0 AINM = DGND.
        self._spi.write_register(self._pi, register, new_value)
        value = self._spi.read_register(self._pi, register)
        print("trw:", hex(new_value), hex(value))
        self.assertEqual(new_value, value)


if __name__ == '__main__':
    unittest.main()
