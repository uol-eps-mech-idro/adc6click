#!/usr/bin/env python3
""" Uses AD7124 driver functions to read a voltage.
This was used to work out how to read the registers of the AD7124 correctly.
"""

import time
import unittest

from ad7124driver import AD7124Driver
from ad7124registers import AD7124RegNames


class TestAD7214Voltmeter(unittest.TestCase):

    # Hardware settings
    POSITION = 1
    INTERNAL_REFERENCE = True
    BIPOLAR = True
    # CHANNEL 0 uses AIN0,1, 1 uses AIN2,3, 2 uses AIN4,5.
    CHANNEL = 1
    # Always uses ADC setup 0.

    def setUp(self):
        """ Verify init works.
        Can throw an exception if the ADC is not connected.
        """
        self._driver = AD7124Driver(self.POSITION)

    def _init_adc(self):
        """ Setup ADC.  These values are taken from the Mikro example code.
            adc6_resetDevice();
            adc6_writeReg( _ADC6_CONFIG_0_REG,
                _ADC6_CONFIG_ENABLE_BIPOLAR_OP |
                _ADC6_CONFIG_ENABLE_BUFFER_ON_AINP |
                _ADC6_CONFIG_ENABLE_BUFFER_ON_AINM );
            adc6_writeReg( _ADC6_CHANNEL_0_REG, _ADC6_ENABLE_CHANNEL |
                _ADC6_CHANNEL_NEGATIVE_ANALOG_INPUT_AIN1 );
            adc6_writeReg( _ADC6_CONTROL_REG,
                _ADC6_CONTROL_DATA_STATUS_ENABLE |
                _ADC6_CONTROL_DOUT_PIN_ENABLE |
                _ADC6_CONTROL_INTERNAL_REFERENCE_VOLTAGE_ENABLE |
                _ADC6_CONTROL_FULL_POWER_MODE );
        """
        self._driver.reset()
        print("Using channel 0, setup 0")
        # Config 0
        register = AD7124RegNames.CFG0_REG
        self._driver.set_setup_config(
            register,
            bipolar=self.BIPOLAR,  # _ADC6_CONFIG_ENABLE_BIPOLAR_OP
            ain_buf_p=True,  # _ADC6_CONFIG_ENABLE_BUFFER_ON_AINP
            ain_buf_m=True  # _ADC6_CONFIG_ENABLE_BUFFER_ON_AINM
        )
        value = self._driver.read_register(register)
        if self.BIPOLAR:
            self.assertEqual(0x0860, value)
        else:
            self.assertEqual(0x0060, value)
        # Configuration Filter Register
        register = AD7124RegNames.FILT0_REG
        self._driver.set_setup_filter(
            register,
            filter_type=0,  # SINC4
            # post_filter=0,  # No post filter.
            post_filter=3,  # Default
            output_data_rate=0x180  # Fastest is 0x001.
        )
        value = self._driver.read_register(register)
        # self.assertEqual(0x000180, value)
        self.assertEqual(0x060180, value)
        # Channel Register
        ainp = 0  # 9:5 0b00000 _ADC6_CHANNEL_POSITIVE_ANALOG_INPUT_AIN0
        ainm = 1  # 4:0 0b00001 _ADC6_CHANNEL_NEGATIVE_ANALOG_INPUT_AIN1
        expected = 0x8001
        if self.CHANNEL == 1:
            ainp = 2
            ainm = 3
            expected = 0x8043
        elif self.CHANNEL == 2:
            ainp = 4
            ainm = 5
            expected = 0x8085
        register = AD7124RegNames.CH0_MAP_REG
        self._driver.set_channel(
            register,
            enable=True,  # 15 _ADC6_CONTROL_DATA_STATUS_ENABLE
            setup=0,  # Setup 0.
            ainp=ainp,
            ainm=ainm
        )
        value = self._driver.read_register(register)
        self.assertEqual(expected, value)
        # Verify that all channels are disabled.
        # This test was added because more than one channel was active.
        # Never found the cause but it has gone away.
        for channel in range(1, 16):
            register_enum = AD7124RegNames(
                            AD7124RegNames.CH0_MAP_REG.value + channel)
            assert_msg = "channel: " + str(channel)
            value = self._driver.read_register(register_enum)
            # print("tv.ia: channel, value", channel, hex(value))
            self.assertEqual(0x0001, value, assert_msg)
        # ADC control register
        self._driver.set_adc_control(
            data_status=True,  # 10 _ADC6_CONTROL_DATA_STATUS_ENABLE
            not_cs_en=True,  # 9 _ADC6_CONTROL_DOUT_PIN_ENABLE
            ref_en=self.INTERNAL_REFERENCE,
            power_mode=2  # 7,6 _ADC6_CONTROL_FULL_POWER_MODE
        )
        register = AD7124RegNames.ADC_CTRL_REG
        new_value = 0
        new_value |= 0x0400  # 10 _ADC6_CONTROL_DATA_STATUS_ENABLE
        new_value |= 0x0200  # 9 _ADC6_CONTROL_DOUT_PIN_ENABLE
        new_value |= 0x0100
        new_value |= 0x0080
        value = self._driver.read_register(register)
        self.assertEqual(new_value, value)
        # Read all registers.
        for register_enum in AD7124RegNames:
            value = self._driver.read_register(register_enum)
            print("Register: ", register_enum.name, hex(value))
        print("Done")

    def _check_errors(self):
        """ Checks for any errors that could prevent the tests running.
        Asserts if something fatal is wrong.
        """
        # Read error register.
        error_reg = self._driver.read_register(AD7124RegNames.ERR_REG)
        self.assertEqual(0, error_reg)

    def test_multiple_reads(self):
        """ Set up ADC to read AIN0 using channel 0 single reads.
        """
        self._init_adc()
        self._check_errors()
        gain = 1
        vref = 1.25
        bipolar = self.BIPOLAR
        scale = 1.0
        start_time = time.time()
        valid_readings = 0
        invalid_readings = 0
        print("\nInitialised.")
        # Start
        for i in range(0, 10):
            time.sleep(0.1)
            # Read data register with status.  Prevents duplicate readings as
            # status = 0x90 when reading the same data for the second time.
            (int_value, status) = self._driver.read_register_with_status(
                                AD7124RegNames.DATA_REG)
            # print("int_value, status", hex(int_value), hex(status))
            invalid = status & 0x80
            # print("invalid", invalid)
            if invalid:
                invalid_readings += 1
            else:
                voltage = self._driver.to_voltage(int_value, gain, vref,
                                                  bipolar, scale)
                print("Voltage: {:2.8}".format(voltage))
                valid_readings += 1
        # Just to say test passed!
        self.assertEqual(1, 1)
        time_taken = time.time() - start_time
        print("Time taken: ", time_taken)
        print("Valid readings: ", valid_readings)
        print("Invalid readings: ", invalid_readings)
        print("Readings per second: ", valid_readings / time_taken)


if __name__ == '__main__':
    unittest.main()
