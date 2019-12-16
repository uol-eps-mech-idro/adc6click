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
        self._channels = []

    def init(self, position):
        """ Initialises the AD7124.
        position is the Pi2 click shield position number, 1 or 2.
        Throws an exception if it fails.
        NOTES:
        The channels and setups use default values that are set when created.
        """
        self._spi.init(self._pi, position)
        for i in range(0, 16):
            channel = AD7124Channel(i)
            self._channels.append(channel)
        for i in range(0, 8):
            setup = AD7124Setup(i)
            self._setups.append(setup)
        self._set_diagnostics()
        clock_select = 0  # Internal clock.
        mode = 0  # Continuous conversion.
        power_mode = 3  # Full power mode.
        self._set_control_register(clock_select, mode, power_mode)

    def term(self):
        """ Terminates the AD7124. """
        self._spi.term(self._pi)
        self._pi.stop()

    def start_continuous_read(self):
        """ TODO """
        result = True
        return result

    def stop_continuous_read(self):
        """ TODO """
        result = True
        return result

    def _set_diagnostics(self):
        """ Setting diagnostics means setting the ERROR_EN register.
        Set the default of 0x000040.
        """
        self._spi.write_register(self._pi, AD7124RegNames.ERREN_REG, 0x000040)

    def _set_control_register(self, clock_select, mode, power_mode):
        """ Writes to the ADC control register.
        Default value of the register is 0x0000 so defaults of 0 work.
        """
        value = 0
        # The control register is 16 bits, MSB first.
        # MSB - for now all 0s, so nothing to do.
        value |= (clock_select & 0x03)
        value |= ((mode & 0x0f) << 2)
        value |= ((power_mode & 0x03) << 6)
        print("write_reg_control to_send", value)
        self._spi.write_register(self._pi, AD7124RegNames.ADC_CTRL_REG, value)

    def read_data_wait(self):
        """ Reads the data register.  Blocks until data is ready.
        """
        ready = False
        timeout = 300
        while not ready and timeout > 0:
            status = self.read_status()
            ready = status[0]
            timeout -= 1
        value = self._spi.read_register(self._pi, AD7124RegNames.DATA_REG)
        print("read_data_wait:", timeout, hex(value))
        return (timeout, value)

    def read_status(self):
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
        #print("read_status", hex(value))
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
