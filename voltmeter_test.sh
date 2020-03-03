#!/bin/bash

if [ ! -e /run/pigpio.pid ]
then
    sudo pigpiod
fi

python3 -m unittest -v test_voltmeter
