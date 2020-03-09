#!/usr/bin/env python3
""" Unit tests for the AD7124 driver. """
import time
import unittest

from ad7124spi import AD7124SPI


class TestAD7214Spi(unittest.TestCase):
    """ Tests the SPI interface functions. """
    PADDING_BYTE = 0xff

    def setUp(self):
        """ Verify init works.
        Can throw an exception if the ADC is not connected.
        """
        position = 1
        self._spi = AD7124SPI(position)
        to_send = b'\xff\xff\xff\xff\xff\xff\xff\xff'
        self._spi.write_register(to_send)
        # Wait for reset to complete.
        time.sleep(0.01)

    def test_read_register(self):
        """ Read the ID register. Should return 0x14.
        """
        to_send = b'\x45\x00'
        (_, result) = self._spi.read_register(to_send)
        self.assertEqual(self.PADDING_BYTE, result[0])
        self.assertEqual(0x14, result[1])

    def test_write_register(self):
        """ Read, modify and read the channel 1 register.
        Read the register.  Should be 0x0001.
        Then write a new value that changes both bytes.
        Read back to verify change has occurred.
        """
        to_send = b'\x4a\x00\x00'
        (_, result) = self._spi.read_register(to_send)
        self.assertEqual(self.PADDING_BYTE, result[0])
        self.assertEqual(0x00, result[1])
        self.assertEqual(0x01, result[2])
        to_send = b'\x0a\x80\x10'
        self._spi.write_register(to_send)
        to_send = b'\x4a\x00\x00'
        (_, result) = self._spi.read_register(to_send)
        self.assertEqual(self.PADDING_BYTE, result[0])
        self.assertEqual(0x80, result[1])
        self.assertEqual(0x10, result[2])


if __name__ == '__main__':
    unittest.main()
