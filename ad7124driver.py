""" AD7124-8 driver using the Mikro ADC6Click board on the Raspberry Pi.
Please install the following packages before first use.
'sudo apt-get install python3-spidev python-spidev python-dev python3-dev'

Based on C code from here:
https://github.com/analogdevicesinc/no-OS/tree/master/drivers/adc/ad7124
"""

import spidev

dev1 = spidev.SpiDev() 

class AD7124Driver:

    def __init__(self):
        """ Initialises the AD7124 device. """
        self.reset()

    def reset(self):
        """ Resets the AD7124 to power up conditions. """
        pass

    def read_register(self, register):
        """ The value of the given register is returned. 
        If the register was not read, returns None.
        """
        result = None
        return result


    def write_register(self, register, data):
        """ The data is wrtten to the given register. 
        Returns True if the value was successfully written.
        """
        result = False
        return result
