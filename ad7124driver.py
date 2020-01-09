#!/usr/bin/env python3
""" AD7124-8 driver using the Mikro ADC6Click board on the Raspberry Pi.
Uses PiGPIO for SPI and GPIO access. http://abyz.me.uk/rpi/pigpio/

Please install the following packages before first use.
TODO


Before running this script, the pigpio daemon must be running.
 sudo pigpiod

"""
import time
import pigpio
from ad7124spi import AD7124SPI
from ad7124channel import AD7124Channel
from ad7124setup import AD7124Setup
from ad7124registers import AD7124RegNames


class AD7124Driver:
    """ Provides a wrapper that hides the SPI calls and many of the
    messy parts of the AD7124 implementation.
    """

    def __init__(self):
        """ Initialise the AD7124 device. """
        self._pi = pigpio.pi()
        self._spi = AD7124SPI()
        self._setups = []
        self._channels = {}

    def init(self, position):
        """ Initialises the AD7124.
        position is the Pi2 click shield position number, 1 or 2.
        Throws an exception if it fails.
        NOTES:
        The channels and setups use default values that are set when created.
        Although this code sets up all channels and setups, only channels 1
        and 2 are enabled.  Channel one uses setup 1. Channel 2 uses setup 2.
        """
        self._spi.init(self._pi, position)
        # This follows the recommended order in the datasheet:
        # channel, setup, diagonostics, control register.
        for i in range(0, 16):
            channel = AD7124Channel(i)
            channel.set(self._pi, self._spi)
            self._channels[i] = channel
        for i in range(0, 8):
            setup = AD7124Setup(i)
            # TODO setup.set(self._pi, self._spi)
            self._setups.append(setup)
        self._set_diagnostics()
        clock_select = 0  # Internal clock.
        mode = 0  # Continuous conversion.
        power_mode = 3  # Full power mode.
        ref_en = 1  # Enable internal reference voltage.
        not_cs_en = 0
        data_status = 0  # Enable status byte for all replies.
        cont_read = 0
        self._set_control_register(clock_select, mode, power_mode,
                                   ref_en, not_cs_en, data_status, cont_read)

    def term(self):
        """ Terminates the AD7124. """
        self._spi.term(self._pi)
        self._pi.stop()

    def read(self, channel_num):
        """ Reads one value from the given channel."""
        voltage = 0.0
        if channel_num < 0 or channel_num > 15:
            raise ValueError("Channel number out of range")
        else:
            channel = self._channels[channel_num]
            voltage = channel.read(self._pi, self._spi)
        return voltage

    def _set_diagnostics(self):
        """ Setting diagnostics means setting the ERROR_EN register.
        Set the default of 0x000040.
        """
        self._spi.write_register(self._pi, AD7124RegNames.ERREN_REG, 0x000040)

    def _set_control_register(self, clock_select, mode, power_mode,
                              ref_en, not_cs_en, data_status, cont_read):
        """ Writes to the ADC control register.
        Default value of the register is 0x0000 so defaults of 0 work.
        """
        value = 0
        # The control register is 16 bits, MSB first.
        if cont_read:
            value |= (1 << 11)
        if data_status:
            value |= (1 << 10)
        if not_cs_en:
            value |= (1 << 9)
        if ref_en:
            value |= (1 << 8)
        value |= ((power_mode & 0x03) << 6)
        value |= ((mode & 0x0f) << 2)
        value |= (clock_select & 0x03)
        print("_set_control_register to_send", hex(value))
        self._spi.write_register(self._pi, AD7124RegNames.ADC_CTRL_REG, value)

    def _read_status(self):
        """ Returns a tuple containing the values:
        (ready {bool}, error{bool}, power on reset{bool}, active channel)
        NOTE: ready = True when ready.  The ADC sets bit 7 to low when ready
        so this code inverts the sense to make it behave as the other flags do.
        """
        # RDY is inverted.
        ready = True
        error = False
        power_on_reset = False
        active_channel = 0
        value = self._spi.read_register(self._pi, AD7124RegNames.STATUS_REG)
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

    def read_data_wait(self):
        """ Reads the data register.  Blocks until data is ready.
        """
        ready = False
        for _ in range(0,300):
            status = self._read_status()
            ready = status[0]
            if ready:
                break
        value = self._spi.read_register(self._pi, AD7124RegNames.DATA_REG)
        print("read_data_wait:", value)
        return value

    def read_one_conversion(self):
        """ Requests conversion on pin AIN1.
        Reads the data register.
        Blocks until data is ready.
        """
        # Control register is set to high power mode, continuous conversion
        # by init().
        # CH1_MAP_REG
        # Enable 15, Setup 14:12 = 1, 9:5 = 00001, 4:0 = 00001
        value = 0b1001000000100001
        self._spi.write_register(self._pi, AD7124RegNames.CH1_MAP_REG, value)
        # Setup 1, config
        # bipolar = 1, the rest = 0.
        value = 0b0000100000000000
        self._spi.write_register(self._pi, AD7124RegNames.CFG1_REG, value)
        # Filter, offset and gain registers leave as default.
        value = self.read_data_wait()
        print("read_single_conversion:", value)
        return value

    def start_continuous_read(self):
        """ TODO """
        result = True
        return result

    def stop_continuous_read(self):
        """ TODO """
        result = True
        return result

