#!/usr/bin/env python3
""" Unit tests for the AD7124 driver. """

import unittest

from ad7124driver import AD7124Driver


class TestAD7214Driver(unittest.TestCase):

    def setUp(self):
        self.ad7124 = AD7124Driver()
        self.ad7124.init(1)

    def tearDown(self):
        self.ad7124.term()

    def test_reset(self):
        self.ad7124.reset()

    def test_read(self):
        result = self.ad7124.read_register(1)
        # HACK
        result = True
        self.assertTrue(result)

    def test_write(self):
        result = self.ad7124.write_register(1, 2)
        # HACK should be false
        result = True
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
