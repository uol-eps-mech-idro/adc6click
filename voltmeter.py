#!/usr/bin/env python3
""" Voltmeter command line utility.
This file uses the AD7124Driver class to set up and control the AD7124 device.
"""

import time
from optparse import OptionParser
from ad7124driver import AD7124Driver
from ad7124registers import AD7124RegNames


class VoltmeterChannel:
    """ Stores the values for a voltmeter channel.
    Not to be confused with the AD7124 channels!
    """
    # VREF is fixed by the hardware so do not change this!
    VREF = 1.25

    def __init__(self, number):
        self._number = number
        # Variables needed for voltage conversion.
        # Defaults are "useful".
        self._gain = 1.0
        self._bipolar = True
        self._scale = 1.0

    def setup(self, adc):
        """ Setup channel.
        Values are hard coded so only channel 1 and 2 are supported.
        """
        if self._number == 1:
            config_reg = AD7124RegNames.CFG1_REG
            filter_reg = AD7124RegNames.FILT1_REG
            channel_reg = AD7124RegNames.CH1_MAP_REG
            setup = 1
            positive_pin = 2
            negative_pin = 3
            self._bipolar = True
            self._scale = 7.5 / self.VREF
        elif self._number == 2:
            config_reg = AD7124RegNames.CFG2_REG
            filter_reg = AD7124RegNames.FILT2_REG
            channel_reg = AD7124RegNames.CH2_MAP_REG
            setup = 2
            positive_pin = 4
            negative_pin = 5
            self._bipolar = False
            self._scale = 10.0 / self.VREF
        else:
            print("ERROR: ONLY CHANNEL 1 AND SUPPORTED")
            exit(-1)
        # Set the registers up
        adc.set_setup_config(config_reg, bipolar=self._bipolar,
                             ref_buf_p=True, ref_buf_m=True,
                             ain_buf_p=True, ain_buf_m=True,
                             ref_sel=0, pga=0)
        # Filters are set up for speed so are less accurate.
        adc.set_setup_filter(
            filter_reg,
            filter_type=0,  # SINC4
            post_filter=0,  # No post filter.
            output_data_rate=0x200  # Fastest is 0x001.
        )
        adc.set_channel(channel_reg, enable=True, setup=setup,
                        ainp=positive_pin, ainm=negative_pin)

    def to_voltage(self, adc, int_value):
        voltage = adc.to_voltage(int_value, self._gain, self.VREF,
                                 self._bipolar, self._scale)
        return voltage


class Voltmeter:
    """ Handles user options to control the "Voltmeter".
    Calls AD7124Driver to setup and read values.
    Outputs the values in the requested format.
    """

    VERSION = "0.1"

    def __init__(self):
        self._csv = False
        self._filename = ""
        self._stdout = False
        # List of VoltmeterChannel instances.
        self._channels = []
        self._position = 1
        self._adc = None
        # Performance stats
        self._start_time = None
        self._readings = 0

    def parse_options(self):
        """ Parse command line arguments and provide user help. """
        usage = "usage: %prog [options] [1] [2]\n"
        usage += "Reads the channels 1 and/or 2 continuously.\n"
        usage += "\tChannel 1 reads -7.5V to +7.5V. \n"
        usage += "\tChannel 2 reads 0V to +10.0V. \n"
        usage += "To stop the program, press Ctrl+c."
        version = "%prog version " + self.VERSION
        parser = OptionParser(usage, version=version)
        parser.set_defaults(filename="ad7124.csv", output="console",
                            position=1)
        parser.add_option("-o", "--file", dest="filename",
                          help="Write to FILE.", metavar="FILE")
        parser.add_option("-f", "--format", dest="format",
                          help="format: csv, console. Default is '%default'.")
        parser.add_option(
            "-p", "--position", dest="1",
            help="Position of the ADC6Click: 1 or 2.  Default is '%default'."
        )
        parser.add_option("-v", "--verbose",
                          action="store_true", dest="verbose")
        (options, requested_channels) = parser.parse_args()
        # print("print options", options, "channels", requested_channels)
        num_requested_channels = len(requested_channels)
        # print("print num_requested_channels", num_requested_channels)
        if num_requested_channels not in (1, 2):
            parser.error("must have at least one channel.")
        else:
            # Create and store each of the channel instances.
            for requested_channel in requested_channels:
                requested_channel_num = int(requested_channel)
                if 0 <= requested_channel_num <= 15:
                    vm_channel = VoltmeterChannel(requested_channel_num)
                    self._channels.append(vm_channel)
                else:
                    parser.error("channel number out of range. 0 to 15 only.")
        if options.position in (1, 2):
            self._position = options.position
        else:
            parser.error("position must be 1 or 2.")
        if options.format:
            output_format = options.format.lower()
            if output_format == "csv":
                self._csv = True
                self._filename = options.filename
                self._stdout = False

    def _initialise_adc(self):
        """ Initialise the ADC and configure to read the enabled
        channels.
        """
        # Initialise the driver.  Asserts if anything fails.
        self._adc = AD7124Driver(self._position)
        # Set up the driver to read values on the selected channels.
        for vm_channel in self._channels:
            vm_channel.setup(self._adc)
        # ADC control register
        # power_mode 2 is full power so goes fastest.
        self._adc.set_adc_control(power_mode=2)

    def _start_stats(self):
        self._start_time = time.time()

    def _write_stats(self):
        time_taken = time.time() - self._start_time
        print("Time taken: ", time_taken)
        print("Readings: ", self._readings)
        print("Readings per second: ", self._readings / time_taken)

    def _write_header(self):
        print("Starting using channels:", self._channels)
        if self._csv:
            # TODO Open file
            print("Open CSV file")

    def _write_value(self, channel_number, int_value):
        if self._stdout:
            voltage = self._channels[channel_number].to_voltage(int_value)
            print("{}, {:2.6}".format(channel_number, voltage))
        if self._csv:
            # TODO Write to file!
            print("{}, {:2.6}".format(channel_number, voltage))

    def _write_footer(self):
        print("Finished.")
        if self._csv:
            # TODO Close file
            print("CSV file closed")

    def run(self):
        """ This function continuously reads the ADC selected channels until
        the user presses ctrl+c.
        """
        print("Starting...")
        self._write_header()
        self._initialise_adc()
        self._start_stats()
        # Try block handles ctrl+c nicely.
        try:
            while True:
                # Read next value (blocks until data read)
                (channel_number, int_value) = self._adc.read_data_wait()
                # Write value to stdout/csv file.
                self._write_value(channel_number, int_value)
        except KeyboardInterrupt:
            print("\nStopping...")
        finally:
            self._adc.term()
            self._write_stats()
            self._write_footer()


def run():
    voltmeter = Voltmeter()
    voltmeter.parse_options()
    voltmeter.run()


if __name__ == '__main__':
    run()
