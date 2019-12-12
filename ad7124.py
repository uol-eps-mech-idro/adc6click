#!/usr/bin/env python3
""" AD7124 command line utility.
This file uses the AD7124Driver class to set up and control the AD7124 device.
"""

from optparse import OptionParser


class AD7124:
    """ """
    def __init__(self):
        self.options = {}
        self.args = []
        self.version = "0.1"

    def parse_options(self):
        """ Parse command line arguments and provide user help. """
        usage = "usage: %prog [options] 1 2\n"
        usage += "Reads the channels 1 and/or 2 continuously.\n"
        usage += "\tChannel 1 reads -5V to +5V. \n"
        usage += "\tChannel 2 reads 0V to 10V."
        version = "%prog version " + self.version
        parser = OptionParser(usage, version=version)
        parser.set_defaults(filename="stdout", output="spaces")
        parser.add_option("-f", "--filename", dest="filename",
                          help="Write to FILE.", metavar="FILE")
        parser.add_option("-o", "--output", dest="output",
                          help="OUTPUT: csv, spaces. Default is '%default'.")
        parser.add_option("-v", "--verbose",
                          action="store_true", dest="verbose")
        (self.options, self.args) = parser.parse_args()
        if len(self.args) != 1:
            parser.error("must have at least one channel.")
        if options.verbose:
            print("reading %s..." % options.filename)

        print("print options", self.options, "args", self.args)


def run():
    ad7124 = AD7124()
    ad7124.parse_options()


if __name__ == '__main__':
    run()
