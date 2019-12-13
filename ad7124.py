#!/usr/bin/env python3
""" AD7124 command line utility.
This file uses the AD7124Driver class to set up and control the AD7124 device.
"""

import time
from optparse import OptionParser
from ad7124driver import AD7124Driver


class AD7124:
    """ Handles user options.
    Calls AD7124Driver to setup and read values.
    Outputs the values in the reqquested format.
    """

    VERSION = "0.1"

    def __init__(self):
        self._csv = False
        self._filename = ""
        self._stdout = False
        self._channels = []
        self._position = 1
        self._adc = AD7124Driver()

    def parse_options(self):
        """ Parse command line arguments and provide user help. """
        usage = "usage: %prog [options] [1] [2]\n"
        usage += "Reads the channels 1 and/or 2 continuously.\n"
        usage += "\tChannel 1 reads -5V to +5V. \n"
        usage += "\tChannel 2 reads 0V to 10V."
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
        (options, self._channels) = parser.parse_args()
        print("print options", options, "channels", self._channels)
        num_channels = len(self._channels)
        print("print num_channels", num_channels)
        if num_channels != 1 and num_channels != 2:
            parser.error("must have at least one channel.")
        if options.position == 1 or options.position == 2:
            self._position = options.position
        else:
            parser.error("position must be 1 or 2.")
        if options.format:
            output_format = options.format.to_lower()
            if output_format == "csv":
                self._csv = True
                self._filename = options.filename
                self._stdout = False
            elif output_format == "console":
                self._stdout = True

    def run(self):
        print("Starting...")
        self._write_header()
        self._adc_init()
        try:
            while True:
                values_list = self._adc_read()
                for values in values_list:
                    self._write_values(values)
                time.sleep(0.010)
        except KeyboardInterrupt:
            print("Stopping...")
        finally:
            self._adc_term()
            self._write_footer()

    def _adc_init(self):
        """ Tell ADC which channels to use.
        Then tell it to start continuous reading.
        """
        #self._adc.init(self._position)
        pass

    def _adc_read(self):
        """ This empties a queue being filled by the ADC driver.
        Returns a list of tuple containing (timestamp, channel1, channel2)
        """
        values = [(102456, 7, 11)]
        return values

    def _adc_term(self):
        #self._adc.term()
        pass

    def _write_header(self):
        print("Starting capture on channels", self._channels)
        if self._stdout:
            # TODO Needs better formatting
            print(timestamp, values)
        if self._csv:
            # TODO Open file
            print("Open CSV file")

    def _write_values(self, values):
        if self._stdout:
            # TODO Needs better formatting
            print(timestamp, values)
        if self._csv:
            # TODO Needs better formatting
            print("Write to CSV", values)

    def _write_footer(self):
        print("Footer")
        if self._csv:
            # TODO Close file
            print("Close CSV file")


def run():
    print("Started.")
    ad7124 = AD7124()
    ad7124.parse_options()
    ad7124.run()
    print("Finished.")


if __name__ == '__main__':
    run()
