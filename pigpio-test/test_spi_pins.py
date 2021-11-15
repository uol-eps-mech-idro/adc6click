#!/usr/bin/env python3

""" This file "waggles" each of the GPIO pins used for SPI in turn.
This can be used to verify that the RPi GPIO pins are functioning correctly.
"""

import time
import pigpio


def test_spi_pin(pin):
    print("test_spi_pin", pin)
    for _ in range(0, 10):
        pi.write(pin, 0)
        time.sleep(0.1)
        pi.write(pin, 1)
        time.sleep(0.1)

def test_spi_miso():
    miso_pin = 9
    print("test_spi_miso")
    value = 0
    while (1):
        new_value = pi.read(miso_pin)
        if value != new_value:
            print("miso to ", new_value)
            value = new_value
        time.sleep(0.2)


# Connect to pigpoid
pi = pigpio.pi()
if pi.connected:
    time.sleep(0.1)
    test_spi_pin(5)
    test_spi_pin(8)
    test_spi_pin(11)
    test_spi_pin(9)
    test_spi_pin(10)
    test_spi_miso()
    print("Tests finished.")
    # Disconnect from pigpoid
    pi.stop()

