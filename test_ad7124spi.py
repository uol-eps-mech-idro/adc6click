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
        self._spi = AD7124SPI()
        position = 1
        self._spi.init(position)

    def tearDown(self):
        self._spi.term()

    def test_read_register(self):
        """ Read the ID register.
        Should return (1, 0x14).
        """
        to_send = b'\x09\x00\x01'
        result = self._spi.read_register(to_send)
        self.assertEqual(1, result[0])
        self.assertEqual(0x14, result[1])

    def test_write_register(self):
        """ Read, modify and read the channel 1 register.
        Read the register.  Should be 0x0001.
        Then write a new value that changes both bytes.
        Read back to verify change has occurred.
        """
        to_send = b'\x5a\x00\x00'
        result = self._spi.read_register(to_send)
        self.assertEqual(2, result[0])
        self.assertEqual(0x0001, result[1])
        to_send = b'\x1a\x80\x10'
        self._spi.write_register(to_send)
        to_send = b'\x5a\x00\x00'
        result = self._spi.read_register(to_send)
        self.assertEqual(2, result[0])
        self.assertEqual(0x8010, result[1])


if __name__ == '__main__':
    unittest.main()
