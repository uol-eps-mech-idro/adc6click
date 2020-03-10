#!/usr/bin/env python3
""" AD7124-8 driver.
Provides functions to read and write to any register and to configure
the AD7124.
"""

import time
from ad7124spi import AD7124SPI  # , bytes_to_string
from ad7124registers import AD7124RegNames, AD7124Registers


class AD7124Driver:
    """ Provides a wrapper that hides the messy parts of the AD7124
    implementation.
    """

    def __init__(self, position):
        """ Initialise the AD7124 device. """
        self._registers = AD7124Registers()
        self._spi = AD7124SPI(position)
        self.reset()
        # Check correct device is present.
        ad7124_id = self.read_id()
        # print("init id", hex(ad7124_id))
        if ad7124_id not in (0x14, 0x16):
            raise OSError('ERROR: device on SPI bus is NOT an AD7124!')

    def _build_command(self, register_enum, read=False):
        """ Builds a command byte.
        First bit (bit 7) must be a 0.
        Second bit (bit 6) is read (1) or write (0).
        Remaining 6 bits are register address.
        """
        command = 0
        if read:
            command += (1 << 6)
        command += (register_enum.value & 0x3f)
        # print("_build_command", hex(command))
        return command

    def _read_register(self, register_enum, status_byte):
        """ Returns the value read from the register as a tuple of:
        count and a list of bytes.
        """
        to_send = []
        command = self._build_command(register_enum, True)
        to_send.append(command)
        # Send correct number of padding bytes to get result.
        num_bytes = self._registers.size(register_enum)
        if status_byte:
            num_bytes += 1
        value = 0
        value_bytes = value.to_bytes(num_bytes, byteorder='big')
        to_send += value_bytes
        (count, result) = self._spi.read_register(to_send)
        # print("_read_register: count", count, "data", result)
        return result

    def _data_to_int(_, data):
        int_value = 0
        # Remove first byte as always 0xFF
        data = data[1:]
        for byte_value in data:
            int_value <<= 8
            int_value |= byte_value
        return int_value

    def reset(self):
        """ Resets the AD7124 to power up conditions. """
        to_send = b'\xff\xff\xff\xff\xff\xff\xff\xff'
        # print("reset command", to_send)
        self._spi.write_register(to_send)
        # TODO WAIT UNTIL PROPERLY READY
        time.sleep(0.001)
        # Disable Channel 0 (enabled by default after reset).
        # 0x0001 is default for the other channel registers.
        value = 0x0001
        register_enum = AD7124RegNames(AD7124RegNames.CH0_MAP_REG.value)
        self.write_register(register_enum, value)

    def read_id(self):
        """ The value of the ID register is returned.
        :returns: The value of the ID register.  Should be 0x14 or 0x16.
        """
        # print("read_id")
        register_enum = AD7124RegNames(AD7124RegNames.ID_REG)
        result = self.read_register(register_enum)
        return result

    def write_register(self, register_enum, value):
        """ Write the given value to the given register.
        :param register_enum: The register to write to,
            e.g. AD7124RegNames.ERREN_REG.
        :param value: The value as an integer.
        """
        # Command value
        to_send = []
        command = self._build_command(register_enum)
        to_send.append(command)
        # Convert value to bytes.
        num_bytes = self._registers.size(register_enum)
        value_bytes = value.to_bytes(num_bytes, byteorder='big')
        to_send += value_bytes
        # Print to_send as hex values for easier debugging.
        # print("write_register: to_send", bytes_to_string(to_send))
        # Write the data.
        self._spi.write_register(to_send)

    def read_register(self, register_enum):
        """ Returns the value read from the register as an int value.
        :param register_enum: The register to read,
            e.g. AD7124RegNames.DATA.
        :returns: integer value of the register contents.
        """
        result = self._read_register(register_enum, False)
        value = self._data_to_int(result)
        # print("read_register: value", hex(value))
        return value

    def read_status(self):
        """ Returns a tuple containing the values:
        (ready{bool}, error{bool}, power on reset{bool}, active channel)
        NOTE: ready = True when ready.  The ADC sets bit 7 to low when ready
        so this code inverts the sense to make it behave as the other flags do.
        """
        # RDY is inverted.
        ready = True
        error = False
        power_on_reset = False
        active_channel = 0
        value = self.read_register(AD7124RegNames.STATUS_REG)
        # print("read_status", hex(value))
        if value & 0x80:
            ready = False
            # print("read_status: ready", ready)
        if value & 0x40:
            error = True
            # print("read_status: error", error)
        if value & 0x10:
            power_on_reset = True
            # print("read_status: power_on_reset", power_on_reset)
        active_channel &= 0x0f
        return (ready, error, power_on_reset, active_channel)

    def read_register_with_status(self, register_enum):
        """ Read the given register returning value and status.
        NOTE: This function should only be used when the DATA_STATUS
        bit of the ADC_CONTROL register is set.
        :param register_enum: The register to read,
            e.g. AD7124RegNames.DATA.
        :returns: A tuple of the value read from the register as an
        int value and the value of the status register.
        """
        result = self._read_register(register_enum, True)
        # Status byte is the last byte.
        value = self._data_to_int(result[:-1])
        status = result[-1]
        # print("read_register_with_status: value:", hex(value),
        #       "status: ", hex(status))
        return (value, status)

    def set_channel(self, register_enum, enable, setup, ainp, ainm):
        """ Sets the given channel register using the given values.
        :param register_enum: The register to set,
            e.g. AD7124RegNames.CH0_MAP_REG.
        :param enable: True to enable the channel.
        :param setup: Number of the setup to use.
        :param ainp: Positive input to use.
        :param ainm: Negative input to use.
        """
        # The channel registers are 16 bits, MSB first.
        value = 0
        # bits 4:0
        value |= (ainm & 0x1f)
        # bits 9:5
        value |= ((ainp & 0x1f) << 5)
        # bits 14:12
        value |= ((setup & 0x07) << 12)
        # bit 15
        if enable:
            value |= 0x8000
        # Write to the register
        print("set_channel_register value:", hex(value))
        self.write_register(register_enum, value)

    def set_setup_config(self, register_enum, bipolar=True, burnout=0,
                         ref_buf_p=False, ref_buf_m=False,
                         ain_buf_p=True, ain_buf_m=True,
                         ref_sel=0, pga=0):
        """ Sets the config register for the setup.
        Defaults set default value in datasheet, 0x0860
        :param register_enum: The register to set, e.g.
            AD7124RegNames.CFG0_REG.
        :param bipolar: True for bipolar, False for unipolar.
        :param burnout: Range 0 to 3. 0 is off.
        :param ref_buf_p: True enabled.
        :param ref_buf_m: True enabled.
        :param ain_buf_p: True enabled.
        :param ain_buf_m: True enabled.
        :param ref_sel: The reference voltage to use. 0 (default) is REFIN1.
        :param pga: Gain select bits. 0 = gain of 1 (default).
        """
        # The configuration registers are 24 bits, MSB first.
        # bits 15:12 must be 0.
        value = 0
        if bipolar:
            value |= 0x0800
        value |= ((burnout & 0x03) << 9)
        if ref_buf_p:
            value |= 0x0100
        if ref_buf_m:
            value |= 0x0080
        if ain_buf_p:
            value |= 0x0040
        if ain_buf_m:
            value |= 0x0020
        value |= ((ref_sel & 0x03) << 3)
        value |= (pga & 0x07)
        print("set_config_register value:", hex(value))
        self.write_register(register_enum, value)

    def set_setup_filter(self, register_enum, filter_type=0, rej60=False,
                         post_filter=6, single_cycle=False,
                         output_data_rate=0x180):
        """ Sets the filter register for the setup.
        Defaults set default value in datasheet, 0x060180
        :param register_enum: The register to set, e.g.
            AD7124RegNames.FILT0_REG.
        :param filter_type: See datasheet for values.
        :param rej60: True is enabled.
        :param post_filter: See datasheet for values.
        :param single_cycle: True is enabled.
        :param output_data_rate: Range 1 to 2047. 1 is fastest but
            noisiest.
        """
        # The filter registers are 24 bits, MSB first.
        # bits 15:11 must be 0.
        value = 0
        value |= ((filter_type & 0x07) << 21)
        if rej60:
            value |= 0x100000
        value |= ((post_filter & 0x07) << 17)
        if single_cycle:
            value |= 0x010000
        value |= (output_data_rate & 0x7ff)
        print("set_filter_register value:", hex(value))
        self.write_register(register_enum, value)

    def set_setup_offset(self, register_enum, new_offset):
        """ Sets the offset register for the setup.
        Defaults set default value in datasheet, 0x800000.
        NOTE: this register is normally set using an internal or
        full-scale calibration.
        :param register_enum: The register to set, e.g.
            AD7124RegNames.OFFS0_REG.
        :param new_offset: The offset value to use.
        """
        # The offset registers are 24 bits, MSB first.
        value = 0
        value |= (new_offset & 0xffffff)
        print("set_setup_offset value:", hex(value))
        self.write_register(register_enum, value)

    def set_setup_gain(self, register_enum, new_gain):
        """ Sets the gain register for the setup.
        Default is a factory generated value.
        NOTE: this register is normally set using an internal or
        full-scale calibration.
        :param register_enum: The register to set, e.g.
            AD7124RegNames.FILT0_REG.
        :param new_gain: The new gain value to apply.
        """
        # The gain registers are 24 bits, MSB first.
        value = 0
        value |= (new_gain & 0xffffff)
        print("set_gain_register value:", hex(value))
        self.write_register(register_enum, value)

    def set_adc_control_register(self, dout_rdy_del=False, cont_read=False,
                                 data_status=False, not_cs_en=False,
                                 ref_en=False, power_mode=0, mode=0,
                                 clock_select=0):
        """ Writes to the ADC control register.
        Default value of the register is 0x0000 so defaults of 0 work.
        """
        value = 0
        # The control register is 16 bits, MSB first.
        # Bits 15:13 must be 0.
        if dout_rdy_del:
            value |= 0x1000
        if cont_read:
            value |= 0x0800
        if data_status:
            value |= 0x0400
        if not_cs_en:
            value |= 0x0200
        if ref_en:
            value |= 0x0100
        value |= ((power_mode & 0x03) << 6)
        value |= ((mode & 0x0f) << 2)
        value |= (clock_select & 0x03)
        print("set_control_register value:", hex(value))
        self.write_register(AD7124RegNames.ADC_CTRL_REG, value)

    # def set_error_register(self, value):
    #     """ Set the ERROR_EN register.
    #     :param value: The value to set (24 bits).
    #     """
    #     self._spi.write_register(AD7124RegNames.ERREN_REG, value)

    # def wait_for_data_ready(self):
    #     """ Blocks until DOUT/!RDY goes low (RDY). """
    #     # TODO
    #     if True:
    #         ready = False
    #         for _ in range(0,300):
    #             status = self._read_status()
    #             ready = status[0]
    #             if ready:
    #                 break
    #     else:
    #         pass

    # def read_data_wait(self):
    #     """ Reads the data register.  Blocks until data is ready.
    #     """
    #     self._wait_for_data_ready()
    #     value = self._spi.read_register_status(self._pi,
    #                                            AD7124RegNames.DATA_REG)
    #     print("read_data_wait:", hex(value[0]), hex(value[1]))
    #     return value[0]

    # def to_voltage(_, int_value, gain, vref, bipolar, scale):
    #     voltage = 0.0
    #     if (bipolar):
    #         voltage = float(int_value / (0x7FFFFF - 1))
    #     else:
    #         voltage = float(int_value / 0xFFFFFF)
    #     voltage = voltage * vref / float(gain)
    #     voltage *= scale
    #     return voltage

    # def to_temperature(self, int_value):
    #     """ Convert ADC value to temperature in degrees Celcius.
    #     """
    #     temperature_c = 0.0
    #     int_value -= 0x800000
    #     # print("channel.read: B", hex(int_value))
    #     temperature_c = float(int_value)
    #     temperature_c /= 13584
    #     # print("channel.read: C", value)
    #     temperature_c -= 272.5
    #     # print("channel.read: D", value)
    #     return temperature_c
