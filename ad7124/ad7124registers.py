""" Classes that define the registers used by the AD7124.
"""

from enum import IntEnum


class AD7124RegNames(IntEnum):
    """ List of all register names.

    IntEnum is used so that basic maths can be done on the enums.
    """

    COMM_REG = 0x00
    STATUS_REG = 0x00
    ADC_CTRL_REG = 0x01
    DATA_REG = 0x02
    IO_CTRL1_REG = 0x03
    IO_CTRL2_REG = 0x04
    ID_REG = 0x05
    ERR_REG = 0x06
    ERREN_REG = 0x07
    CH0_MAP_REG = 0x09
    CH1_MAP_REG = 0x0A
    CH2_MAP_REG = 0x0B
    CH3_MAP_REG = 0x0C
    CH4_MAP_REG = 0x0D
    CH5_MAP_REG = 0x0E
    CH6_MAP_REG = 0x0F
    CH7_MAP_REG = 0x10
    CH8_MAP_REG = 0x11
    CH9_MAP_REG = 0x12
    CH10_MAP_REG = 0x13
    CH11_MAP_REG = 0x14
    CH12_MAP_REG = 0x15
    CH13_MAP_REG = 0x16
    CH14_MAP_REG = 0x17
    CH15_MAP_REG = 0x18
    CFG0_REG = 0x19
    CFG1_REG = 0x1A
    CFG2_REG = 0x1B
    CFG3_REG = 0x1C
    CFG4_REG = 0x1D
    CFG5_REG = 0x1E
    CFG6_REG = 0x1F
    CFG7_REG = 0x20
    FILT0_REG = 0x21
    FILT1_REG = 0x22
    FILT2_REG = 0x23
    FILT3_REG = 0x24
    FILT4_REG = 0x25
    FILT5_REG = 0x26
    FILT6_REG = 0x27
    FILT7_REG = 0x28
    OFFS0_REG = 0x29
    OFFS1_REG = 0x2A
    OFFS2_REG = 0x2B
    OFFS3_REG = 0x2C
    OFFS4_REG = 0x2D
    OFFS5_REG = 0x2E
    OFFS6_REG = 0x2F
    OFFS7_REG = 0x30
    GAIN0_REG = 0x31
    GAIN1_REG = 0x32
    GAIN2_REG = 0x33
    GAIN3_REG = 0x34
    GAIN4_REG = 0x35
    GAIN5_REG = 0x36
    GAIN6_REG = 0x37
    GAIN7_REG = 0x38


class AD7124Registers:
    def __init__(self):
        self._registers = [
            # Initial value, Size, Access Type,  Address
            (0x00, 1, 2),  # 0x00,
            (0x0000, 2, 1),  # 0x01,
            (0x0000, 3, 2),  # 0x02,
            (0x0000, 3, 1),  # 0x03,
            (0x0000, 2, 1),  # 0x04,
            (0x02, 1, 2),  # 0x05,
            (0x0000, 3, 2),  # 0x06,
            (0x0040, 3, 1),  # 0x07,
            (0x00, 1, 2),  # 0x08,
            (0x8001, 2, 1),  # 0x09,
            (0x0001, 2, 1),  # 0x0A,
            (0x0001, 2, 1),  # 0x0B,
            (0x0001, 2, 1),  # 0x0C,
            (0x0001, 2, 1),  # 0x0D,
            (0x0001, 2, 1),  # 0x0E,
            (0x0001, 2, 1),  # 0x0F,
            (0x0001, 2, 1),  # 0x10,
            (0x0001, 2, 1),  # 0x11,
            (0x0001, 2, 1),  # 0x12,
            (0x0001, 2, 1),  # 0x13,
            (0x0001, 2, 1),  # 0x14,
            (0x0001, 2, 1),  # 0x15,
            (0x0001, 2, 1),  # 0x16,
            (0x0001, 2, 1),  # 0x17,
            (0x0001, 2, 1),  # 0x18,
            (0x0860, 2, 1),  # 0x19,
            (0x0860, 2, 1),  # 0x1A,
            (0x0860, 2, 1),  # 0x1B,
            (0x0860, 2, 1),  # 0x1C,
            (0x0860, 2, 1),  # 0x1D,
            (0x0860, 2, 1),  # 0x1E,
            (0x0860, 2, 1),  # 0x1F,
            (0x0860, 2, 1),  # 0x20,
            (0x060180, 3, 1),  # 0x21,
            (0x060180, 3, 1),  # 0x22,
            (0x060180, 3, 1),  # 0x23,
            (0x060180, 3, 1),  # 0x24,
            (0x060180, 3, 1),  # 0x25,
            (0x060180, 3, 1),  # 0x26,
            (0x060180, 3, 1),  # 0x27,
            (0x060180, 3, 1),  # 0x28,
            (0x800000, 3, 1),  # 0x29,
            (0x800000, 3, 1),  # 0x2A,
            (0x800000, 3, 1),  # 0x2B,
            (0x800000, 3, 1),  # 0x2C,
            (0x800000, 3, 1),  # 0x2D,
            (0x800000, 3, 1),  # 0x2E,
            (0x800000, 3, 1),  # 0x2F,
            (0x800000, 3, 1),  # 0x30,
            (0x500000, 3, 1),  # 0x31,
            (0x500000, 3, 1),  # 0x32,
            (0x500000, 3, 1),  # 0x33,
            (0x500000, 3, 1),  # 0x34,
            (0x500000, 3, 1),  # 0x35,
            (0x500000, 3, 1),  # 0x36,
            (0x500000, 3, 1),  # 0x37,
            (0x500000, 3, 1),  # 0x38,
        ]

    # Getters
    def access(self, register_enum):
        """ Returns access type for the given register.
        Args:
            register_enum: The register to look up.
        Returns:
            1 is write, 2 is read.
        """
        # print("registers.access:", register_enum)
        return self._registers[register_enum.value][2]

    def initial(self, register_enum):
        """ Returns initial value of the given register.
        Args:
            register_enum: The register to look up.
        Returns:
            The initial value of the register.
        """
        # print("registers.initial:", register_enum)
        return self._registers[register_enum.value][0]

    def size(self, register_enum):
        """ Returns the size of the given register.
        Args:
            register_enum: The register to look up.
        Returns:
            The number of bytes in the register.
        """
        # print("registers.size:", register_enum)
        return self._registers[register_enum.value][1]
