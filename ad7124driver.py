#!/usr/bin/env python3
""" AD7124-8 driver.
Hides the AD7124 details from the user.
"""

import time
from ad7124spi import AD7124SPI, bytes_to_string
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
        print("init id", hex(ad7124_id))
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
        size = self._registers.size(register_enum)
        num_bytes = self._registers.size(register_enum)
        if status_byte:
            num_bytes += 1
        value = 0
        value_bytes = value.to_bytes(num_bytes, byteorder='big')
        to_send += value_bytes
        (count, result) = self._spi.read_register(to_send)
        print("_read_register: count", count, "data", result)
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
        """ The value of the ID register is returned. """
        # print("read_id")
        register_enum = AD7124RegNames(AD7124RegNames.ID_REG)
        result = self.read_register(register_enum)
        return result

    def write_register(self, register_enum, value):
        """ Write the given value to the given register.
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
        print("write_register: to_send", bytes_to_string(to_send))
        # Write the data.
        self._spi.write_register(to_send)

    def read_register(self, register_enum):
        """ Returns the value read from the register as an int value.
        """
        result = self._read_register(register_enum, False)
        value = self._data_to_int(result)
        print("read_register: value", hex(value))
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
            #print("read_status: ready", ready)
        if value & 0x40:
            error = True
            #print("read_status: error", error)
        if value & 0x10:
            power_on_reset = True
            #print("read_status: power_on_reset", power_on_reset)
        active_channel &= 0x0f
        return (ready, error, power_on_reset, active_channel)


    def read_register_with_status(self, register_enum):
        """ Returns a tuple of the value read from the register as an
        int value and the value of the status register.
        NOTE: This function should only be used when the DATA_STATUS
        bit of the ADC_CONTROL register is set.
        """
        result = self._read_register(register_enum, True)
        # Status byte is the last byte.
        value = self._data_to_int(result[:-1])
        status = result[-1]
        print("read_register_with_status: value:", hex(value),
              "status: ", hex(status))
        return (value, status)

    def set_adc_control(self, clock_select, mode, power_mode,
                              ref_en, not_cs_en, data_status, cont_read):
        """ Writes to the ADC control register.
        Default value of the register is 0x0000 so defaults of 0 work.
        """
        value = 0
        # The control register is 16 bits, MSB first.
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
        print("_set_control_register to_send", hex(value))
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
    #     value = self._spi.read_register_status(self._pi, AD7124RegNames.DATA_REG)
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
