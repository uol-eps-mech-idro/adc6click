#!/usr/bin/env python3
""" Test the  """
import unittest

from ad7124.ad7124registers import AD7124RegNames, AD7124Registers


class TestAD7214RegNames(unittest.TestCase):
    """ Tests the register enum functions. """

    def setUp(self):
        """ Create an instance of all registers.
        """
        self._registers = AD7124Registers()

    def test_getters(self):
        """ Test all getter functions of AD7124Registers.
        """
        # Expected values for ID_REG are:
        # access = 2 - read only.
        # initial = 0x02
        # size = 1
        register_enum = AD7124RegNames.ID_REG
        result = self._registers.access(register_enum)
        self.assertEqual(2, result)
        result = self._registers.initial(register_enum)
        self.assertEqual(0x02, result)
        result = self._registers.size(register_enum)
        self.assertEqual(1, result)
        # Expected values for FILT0_REG are:
        # access =  1 - read/write
        # initial = 0x060180
        # size = 3
        register_enum = AD7124RegNames.FILT0_REG
        result = self._registers.access(register_enum)
        self.assertEqual(1, result)
        result = self._registers.initial(register_enum)
        self.assertEqual(0x060180, result)
        result = self._registers.size(register_enum)
        self.assertEqual(3, result)

    def test_enum_operations(self):
        """ Increment, decrement and add number to AD7124RegNames.
        """
        # Increment
        register_enum = AD7124RegNames.FILT0_REG
        offset = 1
        result = register_enum + offset
        value = register_enum.value + offset
        self.assertEqual(value, result)
        # Decrement
        register_enum = AD7124RegNames.FILT0_REG
        offset = -1
        result = register_enum + offset
        value = register_enum.value + offset
        self.assertEqual(value, result)
        # Add offset
        register_enum = AD7124RegNames.FILT0_REG
        offset = 3
        result = register_enum + offset
        value = register_enum.value + offset
        self.assertEqual(value, result)


if __name__ == "__main__":
    unittest.main()
