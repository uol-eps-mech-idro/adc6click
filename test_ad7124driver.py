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
        Because we have done a reset, power_on_reset should always be
        True.  The other values should be false and active_channel = 0.
        """
        # Do a reset to ensure that power_on_reset is always false.
        self.ad7124.reset()
        time.sleep(0.01)
        # Read the status register.
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
        Expected results: 0x0001 and 0xff.
        Indirectly tests set_adc_control_register.
        """
        self.ad7124.set_adc_control_register(
            dout_rdy_del=False, # No data ready delay.
            cont_read=False,  # Continuous conversion.
            data_status=True,  # Enable data status output.
            not_cs_en=False,  # Controls DOUT/!RDY pin behaviour.
            ref_en=True,  # Internal reference enabled.
            power_mode=3,  # Full power mode.
            mode=0,  # Continuous conversion mode.
            clock_select=0  # Internal clock.
        )
        (value, status) = self.ad7124.read_register_with_status(AD7124RegNames.CH1_MAP_REG)
        self.assertEqual(0x0001, value)
        self.assertEqual(0xff, status)

    def test_set_channel(self):
        """ Set a channel registers with various values.
        Verify that the values read back are the same as written.
        """
        # Enable channel 3 using setup 3 pins 6 and 7.
        register_enum = AD7124RegNames.CH3_MAP_REG
        self.ad7124.set_channel(register_enum, enable=True, setup=3,
                                ainp=6, ainm=7)
        value = self.ad7124.read_register(register_enum)
        expected = 0x8000   # Enable
        expected += 0x3000  # Setup
        expected += 0x00c0  # AINP
        expected += 0x0007  # AINM
        self.assertEqual(expected, value)
        # Enable channel 15 using setup 7 for reading internal temperature.
        register_enum = AD7124RegNames.CH15_MAP_REG
        self.ad7124.set_channel(register_enum, enable=True, setup=7,
                                ainp=16, ainm=16)
        value = self.ad7124.read_register(register_enum)
        expected = 0x8000
        expected += 0x7000
        expected += 0x0200
        expected += 0x0010
        self.assertEqual(expected, value)

    def test_set_setup_config(self):
        """ Set up two setup config registers and verify results.
        """
        # Setup 2, unipolar, burnout 2uA, all bufs on, ref 1, gain = 8.
        register_enum = AD7124RegNames.CFG2_REG
        self.ad7124.set_setup_config(register_enum, bipolar=False, burnout=2,
                                     ref_buf_p=True, ref_buf_m=True,
                                     ain_buf_p=True, ain_buf_m=True,
                                     ref_sel=0, pga=0b011)
        value = self.ad7124.read_register(register_enum)
        expected = 0x0000   # Bipolar off
        expected += 0x0400  # Burnout
        expected += 0x01e0  # All bufs on
        expected += 0x0000  # Ref sel
        expected += 0x0003  # PGA = 8
        self.assertEqual(expected, value)
        # Setup 7, bipolar, no burnout, all bufs off, internal ref, gain = 1.
        register_enum = AD7124RegNames.CFG7_REG
        self.ad7124.set_setup_config(register_enum, bipolar=True,
                                     ref_buf_p=False, ref_buf_m=False,
                                     ain_buf_p=False, ain_buf_m=False,
                                     ref_sel=0b10, pga=0)
        value = self.ad7124.read_register(register_enum)
        expected = 0x0800   # Bipolar on
        expected += 0x0000  # Burnout
        expected += 0x0000  # All bufs off
        expected += 0x0010  # Ref sel
        expected += 0x0000  # PGA = 1
        self.assertEqual(expected, value)



if __name__ == '__main__':
    unittest.main()
