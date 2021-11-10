#!/usr/bin/env python3

""" This file was created so that I could understand how the GPIO pins and
the SPI bus could be controlled using the pigpio library.
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
    data = b'\x45\x00'
    data_read = pi.spi_xfer(spi_h, data)
    print("id should be 0xff14", data_read[1].hex())
    print("id should be 0xff14", data_read[1].hex())
    # Set channel 15 to read temperature. Use setup 7.
    # FIXME
    data = b'\x01\x04\xC0'
    data_read = pi.spi_xfer(spi_h, data)
    print("channel", data_read)
    # Set setup. Leave as default
    # data = b'\x01\x00\x04'
    # data_read = pi.spi_xfer(spi_h, data)
    # print("setup", data_read)
    # Set diagnostics to 0x000040
    # ERREN_REG = 0x07
    data = b'\x07\x00\x00\x40'
    data_read = pi.spi_xfer(spi_h, data)
    # Read
    data = b'\x47\x00\x00\x00'
    data_read = pi.spi_xfer(spi_h, data)
    print("diagnostics", data_read[1].hex())
    # Set control reg
    data = b'\x01\x04\xC0'
    data_read = pi.spi_xfer(spi_h, data)
    # Read
    data = b'\x41\x00\x00'
    data_read = pi.spi_xfer(spi_h, data)
    print("control reg", data_read[1].hex())
    # Read a few times
    for _ in range(0, 1):
        data = b'\x42\x00\x00\x00'
        data_read = pi.spi_xfer(spi_h, data)
        print_temperature(data_read[1])
        # Wait for conversion - fastest is @ 19200Hz or 52uS.
        # 100uS is fine.
        time.sleep(0.1)
    # Tidy up
    pi.spi_close(spi_h)


def print_temperature(adc_value):
    print("print_temperature", adc_value.hex())
    # Convert to int
    int_value = 0
    data = adc_value[1:]
    for byte_value in data:
        int_value <<= 8
        int_value |= byte_value
    # Formula from datasheet.
    int_value -= 0x800000
    temperature = float(int_value)
    temperature /= 13584
    temperature -= 272.5
    print("print_temperature 2:", temperature)


# Connect to pigpoid
pi = pigpio.pi()

if pi.connected:
    test_ad7124_read()
    print("Tests finished.")
    # Disconnect from pigpoid
    pi.stop()
