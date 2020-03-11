#!/usr/bin/env python3
""" Uses AD7124 driver functions to read the internal temperature.
"""

import time
import unittest

from ad7124driver import AD7124Driver
from ad7124registers import AD7124RegNames

DEGREES_CELCIUS=u"\u2103"

class TestAD7214InternalTemperature(unittest.TestCase):

    def setUp(self):
        """ Verify init works.
        Can throw an exception if the ADC is not connected.
        """
        position = 1
        self._adc = AD7124Driver(position)

    def _init_adc(self):
        """ Setup ADC.
        Use channel 15 and setup 7.
        """
        # Config 7. Bipolar. Internal reference.
        register = AD7124RegNames.CFG7_REG
        self._adc.set_setup_config(register, bipolar=True, ref_sel=0b10)
        value = self._adc.read_register(register)
        self.assertEqual(0x0870, value)
        # Configuration Filter Register. Use defaults.
        register = AD7124RegNames.FILT7_REG
        value = self._adc.read_register(register)
        self.assertEqual(0x060180, value)
        # Channel Register
        register = AD7124RegNames.CH15_MAP_REG
        self._adc.set_channel(
            register,
            # Enable using setup 7.
            enable=True, setup=7,
            # Internal temperature sensor
            ainp=0b10000, ainm=0b10000
        )
        value = self._adc.read_register(register)
        expected = 0
        expected |= 0x8000  # Enable
        expected |= 0x7000  # Setup 7
        expected |= 0x0200  # AINP
        expected |= 0x0010  # AINM
        self.assertEqual(expected, value)
        # ADC control register
        self._adc.set_adc_control(
            data_status=False,  # No status message.
            not_cs_en=True,  # DOUT pin.
            ref_en=True,  # Enable internal reference.
            power_mode=2  # Full power mode.
        )
        register = AD7124RegNames.ADC_CTRL_REG
        new_value = 0
        new_value |= 0x0200  # NOT CS_EN
        new_value |= 0x0100  # Reference enable
        new_value |= 0x0080  # Power mode = 2
        value = self._adc.read_register(register)
        self.assertEqual(new_value, value)

    def _check_errors(self):
        """ Checks for any errors that could prevent the tests running.
        Asserts if something fatal is wrong.
        """
        # Read error register.
        error_reg = self._adc.read_register(AD7124RegNames.ERR_REG)
        self.assertEqual(0, error_reg)

    def test_multiple_reads(self):
        """ Set up ADC to read AIN0 using channel 0 single reads.
        """
        self._init_adc()
        self._check_errors()
        start_time = time.time()
        valid_readings = 0
        print("Initialised.")
        # Start
        for i in range(0, 30):
            time.sleep(0.5)
            (_, int_value) = self._adc.read_data_wait()
            temperature = self._adc.to_temperature(int_value)
            print("{:5.2f}{}".format(temperature, DEGREES_CELCIUS))
            valid_readings += 1
        # Just to say test passed!
        self.assertEqual(1, 1)
        time_taken = time.time() - start_time
        print("Time taken: ", time_taken)
        print("Readings: ", valid_readings)
        print("Readings per second: ", valid_readings / time_taken)


if __name__ == '__main__':
    unittest.main()
