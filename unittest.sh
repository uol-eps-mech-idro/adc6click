#!/bin/bash

# Must be new instance of pigpiod for all tests to pass.
sudo killall -q pigpiod
sudo pigpiod

# Run the tests.
python3 -m unittest -v test/test_ad7124spi.py test/test_ad7124driver.py \
	test/test_ad7124registers.py

