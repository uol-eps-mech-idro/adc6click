#!/usr/bin/env python3
""" Uses AD7124 driver functions to read all registers.
This was used to diagnose strange problems.
"""

import time

from ad7124driver import AD7124Driver
from ad7124registers import AD7124RegNames


def setup(self):
    """ Verify init works.
    Can throw an exception if the ADC is not connected.
    """

def check_errors(self):
    """ Checks for any errors that could prevent the tests running.
    Asserts if something fatal is wrong.
    """

def run():
    # Initialise ADC
    position = 1
    driver = AD7124Driver(position)
    # Read error register.
    value = driver.read_register(AD7124RegNames.ERR_REG)
    if value:
        print("Error not zero.")
    else:
        # Read all registers.
        for register_enum in AD7124RegNames:
            value = driver.read_register(register_enum)
            print("Register: ", register_enum.name, hex(value))
        print("Done")

if __name__ == '__main__':
    run()
