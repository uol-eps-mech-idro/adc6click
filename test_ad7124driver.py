#!/usr/bin/env python3
""" Unit tests for the AD7124 driver. """

import time
import unittest
from ad7124driver import AD7124Driver
from ad7124registers import AD7124RegNames


class TestAD7214Driver(unittest.TestCase):

    def setUp(self):
        self.ad7124 = AD7124Driver()
        position = 1
        # Resets ADC, queries ID register and then sets default channel and
        # setup values.
        # Will raise exception if fails.
        self.ad7124.init(position)

    def tearDown(self):
        self.ad7124.term()

    def test_read_status(self):
        """ Verifies the status register.
        After a reset, power on reset will be True.
        The other values should be False, False, 0.
        """
        status = self.ad7124._read_status()
        print("trs", status)
        ready = status[0]
        error = status[1]
        power_on_reset = status[2]
        active_channel = status[3]
        self.assertEqual(False, ready)
        self.assertEqual(False, error)
        self.assertEqual(True, power_on_reset)
        self.assertEqual(0, active_channel)

    def _test_read_one_conversion(self):
        """ Set up the ADC to do a single conversion.
        Read the status register until a conversion occurs.
        Read the value of the conversion.
        """
        value = self.ad7124.read_one_conversion()
        for _ in range(0,10):
            value = self.ad7124.read_data_wait()
            time.sleep(1)

    def test_start_continuous_read(self):
        """ Test thread start, read and stop.
        Then test get_values().
        """
        # Start
        self.ad7124.start_continuous_read()
        # Wait for a few results to be queued.
        time.sleep(5)
        # Stop
        self.ad7124.stop_continuous_read()
        # Get the values.
        values = self.ad7124.get_values()
        num_values = len(values)
        # Check that more than zero values have been written.
        self.assertLess(5, num_values)
        print("Count: ", num_values)
        for value in values:
            time_str = value[0].isoformat()
            print(time_str, value[1], value[2])


if __name__ == '__main__':
    unittest.main()
