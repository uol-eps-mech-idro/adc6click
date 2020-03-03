#!/usr/bin/env python3
""" Uses the SPI driver to read a voltage.
    This was used to work out how to read the registers of the AD7124 correctly.
"""

import time
import pigpio
import unittest

from ad7124spi import AD7124SPI
from ad7124registers import AD7124RegNames


class TestAD7214Voltmeter(unittest.TestCase):

    def setUp(self):
        """ Verify init works.
        Can throw an exception if the ADC is not connected.
        """
        self._pi = pigpio.pi()
        self._spi = AD7124SPI()
        position = 1
        self._spi.init(self._pi, position)

    def tearDown(self):
        self._spi.term(self._pi)
        self._pi.stop()

    def _to_voltage(_, int_value, gain, vref, bipolar, scale):
        """ Data sheet says:
        code = (2^N x AIN x Gain) / VRef
        Differential voltage: 0 = 0x000000, midscale = 0x80000, fullscale = 0xffffff
        code = 2^N-1 x [(AIN x Gain) / VRef + 1]
        Differential voltage: negative fullscale = 0x000000, 0V = 0x80000, positive fullscale = 0xffffff
        where:
        N = 24
        AIN is the analogue input voltage.
        Gain is the gain setting (1 to 128).
        """
        voltage = 0.0
        float_value = float(int_value) * float(vref)
        if (bipolar):
            voltage = float_value / float(0x800000)
            voltage -= float(vref)
        else:
            voltage = float_value / float(0xFFFFFF)
        voltage *= float(gain)
        # voltage *= scale
        return voltage

    def _init_adc(self):
        """ Setup ADC.  These values are taken from the Mikro example code.
            adc6_resetDevice();
            adc6_writeReg( _ADC6_CONFIG_0_REG, _ADC6_CONFIG_ENABLE_BIPOLAR_OP |
                _ADC6_CONFIG_ENABLE_BUFFER_ON_AINP | _ADC6_CONFIG_ENABLE_BUFFER_ON_AINM );
            adc6_writeReg( _ADC6_CHANNEL_0_REG, _ADC6_ENABLE_CHANNEL |
                _ADC6_CHANNEL_NEGATIVE_ANALOG_INPUT_AIN1 );
            adc6_writeReg( _ADC6_CONTROL_REG, _ADC6_CONTROL_DATA_STATUS_ENABLE |
                _ADC6_CONTROL_DOUT_PIN_ENABLE |
                _ADC6_CONTROL_INTERNAL_REFERENCE_VOLTAGE_ENABLE |
                _ADC6_CONTROL_FULL_POWER_MODE );
        """
        register = AD7124RegNames.CFG0_REG
        new_value = 0
        new_value |= 0x0800  # 11 _ADC6_CONFIG_ENABLE_BIPOLAR_OP
        new_value |= 0x0400  # 6 _ADC6_CONFIG_ENABLE_BUFFER_ON_AINP
        new_value |= 0x0200  # 5 _ADC6_CONFIG_ENABLE_BUFFER_ON_AINM
        # new_value |= 0x0010  # 4:3 Internal ref.
        self._spi.write_register(self._pi, register, new_value)
        value = self._spi.read_register(self._pi, register)
        self.assertEqual(new_value, value)
        register = AD7124RegNames.FILT0_REG
        new_value = 0
        new_value |= 0x400000  # 23:21 Filter, SINC3
        new_value |= 0x0003FF  # 10:0 Go fastest 2047
        self._spi.write_register(self._pi, register, new_value)
        value = self._spi.read_register(self._pi, register)
        self.assertEqual(new_value, value)
        register = AD7124RegNames.CH0_MAP_REG
        new_value = 0
        new_value |= 0x8000  # 15 _ADC6_CONTROL_DATA_STATUS_ENABLE
        new_value |= 0x0000  # 9:5 0b00000 _ADC6_CHANNEL_POSITIVE_ANALOG_INPUT_AIN0
        new_value |= 0x0001  # 4:0 0b00001 _ADC6_CHANNEL_NEGATIVE_ANALOG_INPUT_AIN1
        self._spi.write_register(self._pi, register, new_value)
        value = self._spi.read_register(self._pi, register)
        self.assertEqual(new_value, value)
        register = AD7124RegNames.ADC_CTRL_REG
        new_value = 0
        new_value |= 0x0400  # 10 _ADC6_CONTROL_DATA_STATUS_ENABLE
        new_value |= 0x0200  # 9 _ADC6_CONTROL_DOUT_PIN_ENABLE
        new_value |= 0x0100  # 8 _ADC6_CONTROL_INTERNAL_REFERENCE_VOLTAGE_ENABLE
        new_value |= 0x0080  # 7,6 _ADC6_CONTROL_FULL_POWER_MODE
        self._spi.write_register(self._pi, register, new_value)
        value = self._spi.read_register(self._pi, register)
        self.assertEqual(new_value, value)

    def _check_errors(self):
        """ Checks for any errors that could prevent the tests running.
        Asserts if soemthing fatal is wrong.
        """
        # Read error register.
        (int_value, status) = self._spi.read_register_status(self._pi, AD7124RegNames.ERR_REG)
        print("Error register: ", hex(int_value))
        self.assertEqual(0, int_value)

    def test_multiple_reads(self):
        """ Set up ADC to read AIN0 using channel 0 single reads.
        """
        self._init_adc()
        self._check_errors()
        print("Initialised.")
        # Start
        for i in range(0,200):
            #time.sleep(0.02)
            time.sleep(0.01)
            # Read register with status as status enabled in control register.
            (int_value, status) = self._spi.read_register_status(self._pi, AD7124RegNames.DATA_REG)
            gain = 1
            vref = 2.64
            bipolar = True
            scale = 1.0
            voltage = self._to_voltage(int_value, gain, vref, bipolar, scale)
            print("Voltage:", voltage)
        # Just to say test passed!
        self.assertEqual(1, 1)


if __name__ == '__main__':
    unittest.main()