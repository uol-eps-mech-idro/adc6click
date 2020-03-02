#!/usr/bin/env python3
""" Voltmeter command line utility.
This file uses the AD7124Driver class to set up and control the AD7124 device.
"""

import time
from optparse import OptionParser
from ad7124driver import AD7124Driver


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
        # List of ints, one per channel.
        self._channels = []
        self._position = 1
        self._adc = AD7124Driver()

    def parse_options(self):
        """ Parse command line arguments and provide user help. """
        usage = "usage: %prog [options] [1] [2]\n"
        usage += "Reads the channels 1 and/or 2 continuously.\n"
        usage += "\tChannel 1 reads -5V to +5V. \n"
        usage += "\tChannel 2 reads 0V to 10V. \n"
        usage += "To stop the program, press Ctrl+c."
        version = "%prog version " + self.VERSION
        parser = OptionParser(usage, version=version)
        parser.set_defaults(filename="ad7124.csv", output="console",
                            position = 1)
        parser.add_option("-o", "--file", dest="filename",
                          help="Write to FILE.", metavar="FILE")
        parser.add_option("-f", "--format", dest="format",
                          help="format: csv, console. Default is '%default'.")
        parser.add_option("-p", "--position", dest="1",
                          help="Position of the ADC6Click: 1 or 2.  Default is '%default'.")
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
                    self._channels.append(requested_channel_num)
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

    def run(self):
        """ This function continuously reads the ADC selected channels until
        the user presses ctrl+c.
        """
        print("Starting...")
        self._write_header()
        self._adc.init(self._position)
        self._adc.start_continuous_read()
        # Try block handles ctrl+c nicely.
        try:
            while True:
                values = self._adc.get_values()
                for value in values:
                    self._write_value(value)
                # HACK
                time.sleep(1.0)
        except KeyboardInterrupt:
            print("\nStopping...")
        finally:
            self._adc.stop_continuous_read()
            self._adc.term()
            self._write_footer()

    def _write_header(self):
        print("Starting using channels:", self._channels)
        if self._csv:
            # TODO Open file
            print("Open CSV file")

    def _write_value(self, channel_number, value):
        if self._stdout:
            # TODO Needs better formatting
            print("Channel: ", channel_number, "Value:", value)
        if self._csv:
            # TODO Needs better formatting
            print("Write to CSV", channel_number, value)

    def _write_footer(self):
        print("Finished.")
        if self._csv:
            # TODO Close file
            print("Close CSV file")


def run():
    voltmeter = Voltmeter()
    voltmeter.parse_options()
    voltmeter.run()


if __name__ == '__main__':
    run()
