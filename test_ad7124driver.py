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
        Indirectly tests set_adc_control.
        """
        self.ad7124.set_adc_control(
            dout_rdy_del=False,  # No data ready delay.
            cont_read=False,  # Continuous conversion.
            data_status=True,  # Enable data status output.
            not_cs_en=False,  # Controls DOUT/!RDY pin behaviour.
            ref_en=True,  # Internal reference enabled.
            power_mode=3,  # Full power mode.
            mode=0,  # Continuous conversion mode.
            clock_select=0  # Internal clock.
        )
        (value, status) = self.ad7124.read_register_with_status(
                AD7124RegNames.CH1_MAP_REG)
        self.assertEqual(0x0001, value)
        self.assertEqual(0xff, status)

    def test_read_data_wait(self):
        """ Verifies that the read_data_wait function works.
        """
        # Setup to read channel 0.
        self.ad7124.set_channel(AD7124RegNames.CH0_MAP_REG, enable=True,
                                setup=0, ainp=1, ainm=0)
        # The setup registers are used with defaults.
        # Read the data register.
        (channel_number, int_value) = self.ad7124.read_data_wait()
        self.assertEqual(0, channel_number)
        self.assertEqual(0, int_value)

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

    def test_set_setup_filter(self):
        """ Set up two setup filter registers and verify results.
        """
        # Filter 2, sinc4, rej60, no post_filter, single_cycle,
        # data rate = 0x200
        register_enum = AD7124RegNames.FILT2_REG
        self.ad7124.set_setup_filter(register_enum,
                                     filter_type=0,
                                     rej60=True,
                                     post_filter=0,
                                     single_cycle=True,
                                     output_data_rate=0x200)
        value = self.ad7124.read_register(register_enum)
        expected = 0x000000  # Filter type
        expected += 0x100000  # rej60
        expected += 0x000000  # Post filter
        expected += 0x010000  # Single cycle
        expected += 0x000200  # Data rate
        self.assertEqual(expected, value)
        # Filter 7, post filter enabled, post_filter = 6,
        # data rate = 2047 (slowest)
        register_enum = AD7124RegNames.FILT7_REG
        self.ad7124.set_setup_filter(register_enum,
                                     filter_type=0b111,
                                     rej60=False,
                                     post_filter=0b110,
                                     single_cycle=False,
                                     output_data_rate=2047)
        value = self.ad7124.read_register(register_enum)
        expected = 0xe00000  # Filter type
        expected += 0x000000  # rej60
        expected += 0x0c0000  # Post filter
        expected += 0x000000  # Single cycle
        expected += 0x0007ff  # Data rate
        self.assertEqual(expected, value)

    def test_set_setup_offset(self):
        """ Set up two setup offset registers and verify results.
        """
        # Put into standby mode otherwise registers cannot be written to.
        # Use defaults for all but mode.
        self.ad7124.set_adc_control(mode=0b0010)
        # Offset 2, 0x123456
        register_enum = AD7124RegNames.OFFS2_REG
        new_value = 0x123456
        self.ad7124.set_setup_offset(register_enum, new_value)
        value = self.ad7124.read_register(register_enum)
        self.assertEqual(new_value, value)
        # Offset6, 0xbeef00
        register_enum = AD7124RegNames.OFFS6_REG
        new_value = 0xbeef00
        self.ad7124.set_setup_offset(register_enum, new_value)
        value = self.ad7124.read_register(register_enum)
        self.assertEqual(new_value, value)

    def test_set_setup_gain(self):
        """ Set up two setup gain registers and verify results.
        """
        # Put into idle mode otherwise registers cannot be written to.
        # Use defaults for all but mode.
        self.ad7124.set_adc_control(mode=0b100)
        # Gain 2, 0x123456
        register_enum = AD7124RegNames.GAIN2_REG
        new_value = 0x123456
        self.ad7124.set_setup_gain(register_enum, new_value)
        value = self.ad7124.read_register(register_enum)
        self.assertEqual(new_value, value)
        # Gain 6, 0xbeef00
        register_enum = AD7124RegNames.GAIN6_REG
        new_value = 0xbeef00
        self.ad7124.set_setup_gain(register_enum, new_value)
        value = self.ad7124.read_register(register_enum)
        self.assertEqual(new_value, value)

    def test_set_adc_control(self):
        """ Test the ADC CONTROL register with various combinations.
        """
        # Verify default values.
        self.ad7124.set_adc_control()
        value = self.ad7124.read_register(AD7124RegNames.ADC_CTRL_REG)
        expected = 0x0000
        self.assertEqual(expected, value)
        # Set each single bit value in turn.
        # DATA_READY bit 12
        self.ad7124.set_adc_control(dout_rdy_del=True)
        value = self.ad7124.read_register(AD7124RegNames.ADC_CTRL_REG)
        expected = 0x1000
        self.assertEqual(expected, value)
        # CONT_READ can't be directly tested as it puts the ADC into
        # continuous read mode. 0xffff is returned when this happens.
        self.ad7124.set_adc_control(cont_read=True)
        value = self.ad7124.read_register(AD7124RegNames.ADC_CTRL_REG)
        expected = 0xffff
        self.assertEqual(expected, value)
        # Do a reset so we can read the registers again.
        self.ad7124.reset()
        # DATA_STATUS bit 10
        self.ad7124.set_adc_control(data_status=True)
        value = self.ad7124.read_register(AD7124RegNames.ADC_CTRL_REG)
        expected = 0x0400
        self.assertEqual(expected, value)
        # NOT CS_NE bit 9
        self.ad7124.set_adc_control(not_cs_en=True)
        value = self.ad7124.read_register(AD7124RegNames.ADC_CTRL_REG)
        expected = 0x0200
        self.assertEqual(expected, value)
        # REF_EN bit 8
        self.ad7124.set_adc_control(ref_en=True)
        value = self.ad7124.read_register(AD7124RegNames.ADC_CTRL_REG)
        expected = 0x0100
        self.assertEqual(expected, value)
        # POWER_MODE bits 7:6
        self.ad7124.set_adc_control(power_mode=0b11)
        value = self.ad7124.read_register(AD7124RegNames.ADC_CTRL_REG)
        expected = 0x00c0
        self.assertEqual(expected, value)
        # Mode bits 5:2
        #  Full scale calibration.
        self.ad7124.set_adc_control(mode=0b1000)
        #  This takes some time to update the value.
        time.sleep(0.1)
        value = self.ad7124.read_register(AD7124RegNames.ADC_CTRL_REG)
        expected = 0x0020
        self.assertEqual(expected, value)
        #  Give it a lot more time to complete.
        time.sleep(1.0)
        #  Power down mode.
        self.ad7124.set_adc_control(mode=0b0011)
        value = self.ad7124.read_register(AD7124RegNames.ADC_CTRL_REG)
        expected = 0x000c
        self.assertEqual(expected, value)
        # CLK_SEL bits 1:0. External clock.
        self.ad7124.set_adc_control(clock_select=0b11)
        value = self.ad7124.read_register(AD7124RegNames.ADC_CTRL_REG)
        expected = 0x0003
        self.assertEqual(expected, value)

    def test_to_voltage(self):
        """ Test the convert to voltage function.
        """
        # 0v unipolar
        expected = 0.0
        value = self.ad7124.to_voltage(int_value=0, gain=1, vref=2.50,
                                       bipolar=False, scale=1.0)
        self.assertAlmostEqual(expected, value, 5)
        # Mid scale unipolar
        expected = 1.25
        value = self.ad7124.to_voltage(int_value=0x800000, gain=1, vref=2.50,
                                       bipolar=False, scale=1.0)
        self.assertAlmostEqual(expected, value, 5)
        # Full scale unipolar
        expected = 2.50
        value = self.ad7124.to_voltage(int_value=0xffffff, gain=1, vref=2.50,
                                       bipolar=False, scale=1.0)
        self.assertAlmostEqual(expected, value, 5)
        # Max -ve bipolar
        expected = -1.25
        value = self.ad7124.to_voltage(int_value=0, gain=1, vref=1.25,
                                       bipolar=True, scale=1.0)
        self.assertAlmostEqual(expected, value, 5)
        # 0v bipolar
        expected = 0.0
        value = self.ad7124.to_voltage(int_value=0x800000, gain=1, vref=1.25,
                                       bipolar=True, scale=1.0)
        self.assertAlmostEqual(expected, value, 5)
        # Max +ve bipolar
        expected = +1.25
        value = self.ad7124.to_voltage(int_value=0xffffff, gain=1, vref=1.25,
                                       bipolar=True, scale=1.0)
        self.assertAlmostEqual(expected, value, 5)
        # Max +ve bipolar with gain
        expected = +1.25 / 16.0
        value = self.ad7124.to_voltage(int_value=0xffffff, gain=16, vref=1.25,
                                       bipolar=True, scale=1.0)
        self.assertAlmostEqual(expected, value, 5)
        # Max +ve bipolar scaled to +/-12.5V
        expected = -12.5
        value = self.ad7124.to_voltage(int_value=0x0, gain=1, vref=1.25,
                                       bipolar=True, scale=10.0)
        self.assertAlmostEqual(expected, value, 5)
        expected = +12.5
        value = self.ad7124.to_voltage(int_value=0xffffff, gain=1, vref=1.25,
                                       bipolar=True, scale=10.0)
        self.assertAlmostEqual(expected, value, 5)

    def _value_to_temperature(_, int_value):
        """ Formula from data sheet. """
        return ((int_value - 0x800000)/13584) - 272.5

    def _temperature_to_value(_, temperature_c):
        return int((((temperature_c + 272.5) * 13584) + 0x800000))

    def test_to_temperature(self):
        """ Test the convert to temperature function.
        """
        # 0 scale: -890C
        expected = self._value_to_temperature(0x000000)
        # print("temp:", expected)
        value = self.ad7124.to_temperature(int_value=0x0)
        self.assertAlmostEqual(expected, value, 1)
        # Half scale: -272.5C
        expected = self._value_to_temperature(0x800000)
        # print("temp:", expected)
        value = self.ad7124.to_temperature(int_value=0x800000)
        self.assertAlmostEqual(expected, value, 5)
        # Full scale: 345C
        expected = self._value_to_temperature(0xffffff)
        # print("temp:", expected)
        value = self.ad7124.to_temperature(int_value=0xffffff)
        self.assertAlmostEqual(expected, value, 5)
        # Room temp: 25C, int_value 0xbdaa18
        expected = 25.0
        int_value = self._temperature_to_value(expected)
        # print("temp:", expected, hex(int_value))
        value = self.ad7124.to_temperature(int_value)
        self.assertAlmostEqual(expected, value, 5)


if __name__ == '__main__':
    unittest.main()
