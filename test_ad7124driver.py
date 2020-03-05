#!/usr/bin/env python3
""" Unit tests for the AD7124 driver. """

import time
import unittest
from ad7124driver import AD7124Driver
from ad7124registers import AD7124RegNames


class TestAD7214Driver(unittest.TestCase):
    """ Tests for each API function of the AD7124Driver class. """

    def setUp(self):
        """ Resets ADC, queries ID register.
        Will raise exception if fails.
        """
        position = 1
        self.ad7124 = AD7124Driver(position)

    def test_read_id(self):
        """ Read the ID from the AD7124.
        Expected result: 0x14 or 0x16.
        """
        id = self.ad7124.read_id()
        self.assertIn(id, (0x14, 0x16))

    def test_reset(self):
        """ Reset the AD7124.
        The reset function changes the default for channel 0 to disabled.  This
        proves that it has done the "right thing".
        """
        self.ad7124.reset()
        value = self.ad7124.read_register(AD7124RegNames.CH0_MAP_REG)
        self.assertEqual(0x0001, value)

    def test_read_status(self):
        """ Verifies the status register.
        After a reset, power on reset will be True.
        The other values should be False, False, 0.
        """
        status = self.ad7124.read_status()
        # print("trs", status)
        ready = status[0]
        error = status[1]
        power_on_reset = status[2]
        active_channel = status[3]
        self.assertEqual(False, ready)
        self.assertEqual(False, error)
        self.assertEqual(True, power_on_reset)
        self.assertEqual(0, active_channel)

    def test_read_register_with_status(self):
        """ Read the CH1 register with status.
        Should be 0x0001 and 0xff.
        """
        clock_select = 0  # Internal clock.
        mode = 0  # Continuous conversion mode.
        power_mode = 3  # Full power mode.
        ref_en = True  # Internal reference enabled.
        not_cs_en = False  # Controls DOUT/!RDY pin behaviour.
        data_status = True  # Enable data status output.
        cont_read = False  # Continuous conversion.
        self.ad7124.set_adc_control(clock_select, mode, power_mode, ref_en, not_cs_en, data_status, cont_read)
        (value, status) = self.ad7124.read_register_with_status(AD7124RegNames.CH1_MAP_REG)
        self.assertEqual(0x0001, value)
        self.assertEqual(0xff, status)

    # def _test_read_one_conversion(self):
    #     """ Set up the ADC to do a single conversion.
    #     Read the status register until a conversion occurs.
    #     Read the value of the conversion.
    #     """
    #     value = self.ad7124.read_one_conversion()
    #     for _ in range(0,10):
    #         value = self.ad7124.read_data_wait()
    #         time.sleep(1)




if __name__ == '__main__':
    unittest.main()
