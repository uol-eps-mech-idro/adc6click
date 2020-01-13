#!/usr/bin/env python3
""" AD7124-8 driver using the Mikro ADC6Click board on the Raspberry Pi.
Uses PiGPIO for SPI and GPIO access. http://abyz.me.uk/rpi/pigpio/

Please install the following packages before first use.
TODO


Before running this script, the pigpio daemon must be running.
 sudo pigpiod

"""
import time
from threading import Thread
from threading import Thread
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
        self._read_thread = None
        self._read_thread_running = False

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
        # Channel 1: pin AIN1, setup 1, scale 1.0, unipolar
        channel = AD7124Channel(1, 1, 1, 1.0, unipolar=True)
        channel.set(self._pi, self._spi)
        self._channels[1] = channel
        # Channel 2: pin AIN2, setup 2, scale 1.0, bipolar
        channel = AD7124Channel(2, 2, 2, 1.0, bipolar=True)
        channel.set(self._pi, self._spi)
        self._channels[2] = channel
        # Channel 15: pin AIN15, setup 7, scale 1.0, temperature
        channel = AD7124Channel(15, 2, 2, 1.0, temperature=True)
        channel.set(self._pi, self._spi)
        self._channels[15] = channel
        # Ranges: TODO setup properly.
        for i in range(0, 8):
            setup = AD7124Setup(i)
            setup.set(self._pi, self._spi)
            self._setups.append(setup)
        self._set_diagnostics()
        clock_select = 0  # Internal clock.
        mode = 0  # Continuous conversion = 0.
        power_mode = 3  # Full power mode.
        ref_en = True  # Enable internal reference voltage.
        not_cs_en = False
        data_status = True  # Enable status byte for all replies.
        cont_read = False
        self._set_control_register(clock_select, mode, power_mode,
                                   ref_en, not_cs_en, data_status, cont_read)

    def term(self):
        """ Terminates the AD7124. """
        self._spi.term(self._pi)
        self._pi.stop()

    def read(self, channel_num):
        """ Reads one value from the given channel."""
        voltage = 0.0
        if 0 <= channel_num <=15:
            channel = self._channels[channel_num]
            voltage = channel.read(self._pi, self._spi)
        else:
            raise ValueError("Channel number out of range")
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

    def _wait_for_data_ready(self):
        """ Blocks until DOUT/!RDY goes low (RDY). """
        # TODO
        if True:
            ready = False
            for _ in range(0,300):
                status = self._read_status()
                ready = status[0]
                if ready:
                    break
        else:
            pass

    def read_data_wait(self):
        """ Reads the data register.  Blocks until data is ready.
        """
        self._wait_for_data_ready()
        value = self._spi.read_register_status(self._pi, AD7124RegNames.DATA_REG)
        print("read_data_wait:", hex(value[0]), hex(value[1]))
        return value

    def read_one_conversion(self):
        """ Requests conversion on pin AIN1.
        Blocks until data is ready and then reads the data register.
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
        """ Starts a thread that reads the data register continuously.
        The ADC continuous read mode is enabled.
        Results are placed the queue associated with each channel so they can
        be read asynchronously.
        """
        self._read_thread_running = True
        self._read_thread = Thread(target = self._read_continuously)
        self._read_thread.start()

    def _read_continuously(self):
        """ """
        print("_read_continuously started...")
        # Enable continuous read mode.  Set the CONT_READ bit.
        value = self._spi.read_register(self._pi, AD7124RegNames.ADC_CTRL_REG)
        value |= 0x0800
        self._spi.write_register(self._pi, AD7124RegNames.ADC_CTRL_REG, value)
        # Repeat until told to quit
        while self._read_thread_running:
            # Wait for read
            value, status = self.read_data_wait()
            channel_num = status & 0x0f
            print("thread read cont: channel:", channel_num, "value:", value)
            # Post value to queue
            # channel = self._channels[channel_num]
            # channel.post(value)
            # FIXME: Would be better to wait for !RDY interrupt.
            time.sleep(0.01)
        # Reset ADC to
        self._spi.reset(self._pi)
        print("_read_continuously finished.")

    def stop_continuous_read(self):
        """ Kills the thread. """
        result = True
        # Tell thread to stop
        self._read_thread_running = False
        # Wait for thread to join.
        self._read_thread.join()
        return result
