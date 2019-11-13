#!/usr/bin/env python3
""" Unit tests for the AD7124 driver. """

import unittest

from ad7124driver import AD7124Driver


class TestAD7214Driver(unittest.TestCase):

    def test_reset(self):
        ad7124 = AD7124Driver()
        ad7124.reset()

    def test_read(self):
        ad7124 = AD7124Driver()
        result = ad7124.read_register(1)
        self.assertTrue(result)

    def test_write(self):
        ad7124 = AD7124Driver()
        result = ad7124.write_register(1, 2)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
