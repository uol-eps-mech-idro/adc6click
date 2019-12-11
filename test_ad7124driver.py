#!/usr/bin/env python3
""" Unit tests for the AD7124 driver. """

import unittest

from ad7124driver import AD7124Driver
from ad7124registers import AD7124RegNames


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
        # Channel 0 default is continuous reading in bipolar mode.
        channel_number = 0
        self.ad7124.configure(channel_number)
        for _ in range(0, 5):
            voltage = self.ad7124.read_voltage(channel_number)
            # Assumes disconnected input floats around 0 Volts.
            self.assertAlmostEqual(voltage, 0.0)

    def test_read(self):
        """ Reads the channel 0 register.  After a reset, it will return
        0x8001.
        """
        self.ad7124.reset()
        result = self.ad7124.read_register(AD7124RegNames.CH0_MAP_REG)
        value = int(result[0])
        self.assertEqual(0x80, value)
        value = int(result[1])
        self.assertEqual(0x01, value)

    def test_read_status(self):
        """ Reads the status register. """
        status = self.ad7124.read_status()
        ready = status[0]
        error = status[1]
        power_on_reset = status[2]
        active_channel = status[3]
        self.assertEqual(True, ready)
        self.assertEqual(False, error)
        self.assertEqual(False, power_on_reset)
        self.assertEqual(0, active_channel)

    @unittest.expectedFailure
    def test_write(self):
        result = self.ad7124.write_register(1, 2)
        self.assertTrue(result)


if __name__ == '__main__':
    unittest.main()
