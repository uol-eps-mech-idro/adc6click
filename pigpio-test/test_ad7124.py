#!/usr/bin/env python3

""" This file was created so that I could understand how the GPIO pins and
the SPI bus could be controlled using the pigpio library.
Asks for the ID of the AD7124.
"""

import time
import pigpio


def test_ad7124_read():
    print("test_spi")
    baud = 50 * 1000
    spi_channel = 0
    spi_flags = 3
    time.sleep(0.0001)
    # Open SPI device
    spi_h = pi.spi_open(spi_channel, baud, spi_flags)
    print("Ask for device ID. Expect 20(0x14) or 22(0x16)")
    data = b'\x45\x00'
    data_read = pi.spi_xfer(spi_h, data)
    print("Result: ", data_read)
    pi.spi_close(spi_h)

# Connect to pigpoid
pi = pigpio.pi()

if pi.connected:
    test_ad7124_read()
    print("Tests finished.")
    # Disconnect from pigpoid
    pi.stop()

