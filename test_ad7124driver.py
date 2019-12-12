#!/usr/bin/env python3
""" Unit tests for the AD7124 driver. """

import time
import unittest

from ad7124driver import AD7124Driver
from ad7124registers import AD7124RegNames


callback_count = 0

def callback():
    callback_count += 1

def callback_reset():
    callback_count = 0
from ad7124registers import AD7124RegNames

def callback_get():
    return callback_count

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
        Need to ensure that the active channel is 0.
        """
        status = self.ad7124.read_status()
        print("trs", status)
        ready = status[0]
        error = status[1]
        power_on_reset = status[2]
        active_channel = status[3]
        self.assertEqual(False, ready)
        self.assertEqual(False, error)
        self.assertEqual(True, power_on_reset)
        self.assertEqual(0, active_channel)

    @unittest.expectedFailure
    def test_start(self):
        # assign callback
        callback_reset()
        result = self.ad7124.start(callback)
        self.assertTrue(result)
        # sleep for time for callback to happen.
        time.sleep(0.1)
        # Verify callback variable has been incremented at lest once.
        callback_count = callback_get()
        self.assertGreat(callback_count, 0)

    @unittest.expectedFailure
    def test_stop(self):
        # Stop the read.
        result = self.ad7124.stop(callback)
        self.assertTrue(result)
        # Wait for time to ensure that callbacks stop.
        time.sleep(0.1)
        # Reset variable.
        callback_reset()
        # Wait for time
        time.sleep(0.1)
        # Verify that variable has not been changed.
        callback_count = callback_get()
        self.assertEqual(callback_count, 0)


if __name__ == '__main__':
    unittest.main()
