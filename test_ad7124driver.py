#!/usr/bin/env python3
""" Unit tests for the AD7124 driver. """

import unittest

from ad7124driver import AD7124Driver


class TestAD7214Driver(unittest.TestCase):

    def setUp(self):
        self.ad7124 = AD7124Driver()
        position = 1
        # Verifies that ADC is present by reading Id register.
        # Will raise exception if fails.
        self.ad7124.init(position)

    def tearDown(self):
        self.ad7124.term()

    def test_reset(self):
        self.ad7124.reset()

    def test_read_voltage(self):
        self.ad7124.configure()
        # Channel 0 default is continuous reading in bipolar mode.
        channel_number = 0
        voltage = self.ad7124.read_voltage(channel_number)
        # Assumes disconnected input floats around 0 Volts.
        self.assertAlmostEqual(voltage, 0.0)

    @unittest.expectedFailure
    def test_read(self):
        result = self.ad7124.read_register(1)
        self.assertTrue(result)

    @unittest.expectedFailure
    def test_write(self):
        result = self.ad7124.write_register(1, 2)
        self.assertTrue(result)

if __name__ == '__main__':
    unittest.main()
