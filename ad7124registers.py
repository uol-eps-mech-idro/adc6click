""" Class that defines the registers used by the AD7124.
"""

class AD7124Registers:

    def __init__(self):
        _registers = {
            # Name,                  Address, Initial value, Size, Access Type
            {'AD7124_COMM_REG',     : (0x00,    0x00,          1,    2),
            {'AD7124_STATUS_REG',   : (0x00,    0x0000,        2,    1),
            {'AD7124_ADC_CTRL_REG', : (0x01,    0x0000,        3,    2),
            {'AD7124_DATA_REG',     : (0x02,    0x0000,        3,    1),
            {'AD7124_IO_CTRL1_REG', : (0x03,    0x0000,        2,    1),
            {'AD7124_IO_CTRL2_REG', : (0x04,    0x02,          1,    2),
            {'AD7124_ID_REG',       : (0x05,    0x0000,        3,    2),
            {'AD7124_ERR_REG',      : (0x06,    0x0040,        3,    1),
            {'AD7124_ERREN_REG',    : (0x07,    0x00,          1,    2),
            {'AD7124_CH0_MAP_REG',  : (0x09,    0x8001,        2,    1),
            {'AD7124_CH1_MAP_REG',  : (0x0A,    0x0001,        2,    1),
            {'AD7124_CH2_MAP_REG',  : (0x0B,    0x0001,        2,    1),
            {'AD7124_CH3_MAP_REG',  : (0x0C,    0x0001,        2,    1),
            {'AD7124_CH4_MAP_REG',  : (0x0D,    0x0001,        2,    1),
            {'AD7124_CH5_MAP_REG',  : (0x0E,    0x0001,        2,    1),
            {'AD7124_CH6_MAP_REG',  : (0x0F,    0x0001,        2,    1),
            {'AD7124_CH7_MAP_REG',  : (0x10,    0x0001,        2,    1),
            {'AD7124_CH8_MAP_REG',  : (0x11,    0x0001,        2,    1),
            {'AD7124_CH9_MAP_REG',  : (0x12,    0x0001,        2,    1),
            {'AD7124_CH10_MAP_REG', : (0x13,    0x0001,        2,    1),
            {'AD7124_CH11_MAP_REG', : (0x14,    0x0001,        2,    1),
            {'AD7124_CH12_MAP_REG', : (0x15,    0x0001,        2,    1),
            {'AD7124_CH13_MAP_REG', : (0x16,    0x0001,        2,    1),
            {'AD7124_CH14_MAP_REG', : (0x17,    0x0001,        2,    1),
            {'AD7124_CH15_MAP_REG', : (0x18,    0x0001,        2,    1),
            {'AD7124_CFG0_REG',     : (0x19,    0x0860,        2,    1),
            {'AD7124_CFG1_REG',     : (0x1A,    0x0860,        2,    1),
            {'AD7124_CFG2_REG',     : (0x1B,    0x0860,        2,    1),
            {'AD7124_CFG3_REG',     : (0x1C,    0x0860,        2,    1),
            {'AD7124_CFG4_REG',     : (0x1D,    0x0860,        2,    1),
            {'AD7124_CFG5_REG',     : (0x1E,    0x0860,        2,    1),
            {'AD7124_CFG6_REG',     : (0x1F,    0x0860,        2,    1),
            {'AD7124_CFG7_REG',     : (0x20,    0x0860,        2,    1),
            {'AD7124_FILT0_REG',    : (0x21,    0x060180,      3,    1),
            {'AD7124_FILT1_REG',    : (0x22,    0x060180,      3,    1),
            {'AD7124_FILT2_REG',    : (0x23,    0x060180,      3,    1),
            {'AD7124_FILT3_REG',    : (0x24,    0x060180,      3,    1),
            {'AD7124_FILT4_REG',    : (0x25,    0x060180,      3,    1),
            {'AD7124_FILT5_REG',    : (0x26,    0x060180,      3,    1),
            {'AD7124_FILT6_REG',    : (0x27,    0x060180,      3,    1),
            {'AD7124_FILT7_REG',    : (0x28,    0x060180,      3,    1),
            {'AD7124_OFFS0_REG',    : (0x29,    0x800000,      3,    1),
            {'AD7124_OFFS1_REG',    : (0x2A,    0x800000,      3,    1),
            {'AD7124_OFFS2_REG',    : (0x2B,    0x800000,      3,    1),
            {'AD7124_OFFS3_REG',    : (0x2C,    0x800000,      3,    1),
            {'AD7124_OFFS4_REG',    : (0x2D,    0x800000,      3,    1),
            {'AD7124_OFFS5_REG',    : (0x2E,    0x800000,      3,    1),
            {'AD7124_OFFS6_REG',    : (0x2F,    0x800000,      3,    1),
            {'AD7124_OFFS7_REG',    : (0x30,    0x800000,      3,    1),
            {'AD7124_GAIN0_REG',    : (0x31,    0x500000,      3,    1),
            {'AD7124_GAIN1_REG',    : (0x32,    0x500000,      3,    1),
            {'AD7124_GAIN2_REG',    : (0x33,    0x500000,      3,    1),
            {'AD7124_GAIN3_REG',    : (0x34,    0x500000,      3,    1),
            {'AD7124_GAIN4_REG',    : (0x35,    0x500000,      3,    1),
            {'AD7124_GAIN5_REG',    : (0x36,    0x500000,      3,    1),
            {'AD7124_GAIN6_REG',    : (0x37,    0x500000,      3,    1),
            {'AD7124_GAIN7_REG',    : (0x38,    0x500000,      3,    1)
        }
    
    # Getters
    def address(self, register_name):
        register = self._registers(register_name)
        return register[0]

    def initial(self, register_name):
        register = self._registers(register_name)
        return register[1]
    
    def size(self, register_name):
        register = self._registers(register_name)
        return register[2]

    def access(self, register_name):
        """ Returns access type, 1 is write, 2 is read. """
        register = self._registers(register_name)
        return register[3]
