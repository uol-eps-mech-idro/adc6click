# Design Notes

A collection of notes that were written during development.

## ADC 6 Click Connections

This table shows the connections from the AD7124 to Raspberry Pi via the
mikroBUS™ socket and the Pi2 click shield.

    AD7124                  | mikroBUS™ | Raspberry Pi
    Name              Pin   | Pin Name  | Pin  Notes
    ---------------------------------------------------------
                      NC    | 1   AN    |  7   GPIO4
                            |           | 33   GPIO13
    Synchronization   SYN   | 2   RST   | 29   GPIO5
                            |           | 35   GPIO19
    SPI Chip Select   CS    | 3   CS    | 24   GPIO8/CS0
                            |           | 26   GPIO7/CS1
    SPI Clock         SCK   | 4   SCK   | 23   GPIO11/SPI-SCK
    SPI Data Out/RDY  SDO   | 5   MISO  | 21   GPIO9/SPI-MISO
    SPI Data In       SDI   | 6   MOSI  | 19   GPIO10/SPI-MOSI
    Power supply      +3.3V | 7   +3.3V | 1,17 +3.3V
    Ground            GND   | 8   GND   | 6,9,14,20,25,30,34,39 GND

NOTES

1. Only pins 1 to 8 of the mikroBus are used, the others are all not
connected so are not shown.
1. The Pi2 click shield has two positions for the ADC.  Most connections
to the Raspberry Pi are shared but 3 are not.  Where there are two
entries for a mikroBus pin, the top one is position 1.
1. Max SPI speed is limited by the SCK high and low pulse times, 100ns
for each (datasheet t3 and t4 times), so 200ns per cycle = 5MHz.

## Concepts

The AD7124 has the following key concepts.

* SPI communications are mode 3.
* All communications begin by writing one byte to the communications
register.
* The ID register is used to verify the device type.
* There are 16 channels that can use any one of 8 setups.

## Development

One thing you will notice as you look through the code is numerous commented
out print statements.  These were used during development and have been
intentionally left in the code in case they are needed again.

### Analog Devices Source Code

I started out trying to use the spidev Python package but it is poorly
documented and does not do what I expected it to do.  So I started with the
Analog Devices C driver example.

https://wiki.analog.com/resources/tools-software/uc-drivers/ad7124

Source code from here:
https://github.com/analogdevicesinc/no-OS/tree/master/drivers/adc/ad7124

Added this code to the repo.  Needed SPI and GPIO so found the
platform_drivers.c/h files and wrote a test program to drive it.  It worked
apart from the resulting app has SCLK and CE0 swapped.  Tried to figure out how
to fix this but it started getting deeply into Linux device trees, so I gave up
and tried PiGPIO instead.

### PiGPIO

Copied my test code over from the nRF905Py driver and hacked it to verify the
mode of operation.  Initially, tried to read the Id register as this was
recommended in the docs.  No response.  Tried to read an ADC register and it
came back with numbers.  Figured out that I wasn't setting a read bit when I was
trying to read the ID.  Fixed the code and it works.

One problem with this approach is that the PiGPIO code does not correctly
handle the DataReady signal that the ADC uses to say that data is ready for
reading.  The DataReady signal needs to be used correctly for the continuous
read mode.  In single read mode, the sampling rate is limited to about 8000
samples per second.

### ADC development

Once I could talk to the ADC, setting it up to read values was more tricky than
I expected.  It took a good while to get values from the ADC and when I did they
were not what I expected.  Eventually, I tracked this problem down to a wiring
issue and once solved, I was able to get reliable readings from the device.

The most helpful code that I found was the code in the ardunio-code directory.
However, the voltage conversion function Ad7124Chip::toVoltage() did not work
correctly so I had to re-write that.

There were several problems that delayed development.

One of the key problems was the lack of a circuit diagram for the ADC when used
in split power supply mode.  This caused a lot of time to be spent working out
what did work and what didn't.

Another was strange behaviour (as the input voltage was increased, values
started going up then went down) when the internal voltage reference was not
set up correctly.  This was found to be a hardware problem.

Another was that the input voltage needed to be related to ADC ground, not
just the difference across the analogue input pins. If the voltage was
outside the input maximum range, clamp diodes inside the ADC protect the
device and drastically change the input impedance.

## Phase 1

For the first phase of implementation, we need to measure the following voltage
ranges:

* +/-7V - pendulum tribometer from the charge amplifiers.
* 0 to 9V - TODO get name. Blue machine!

So the plan is to create two inputs, one for the +/-7V and the other for the
0 to 9V measurements.  There will be scaling applied at the inputs in the form
of a fixed potential divider network to scale the input voltages to a range
that the ADC can use.

So what needs to be done is to configure two channels, each connected to
its own input pin and using its own setup.  Then we need to be able to start
and stop the continuous reading of both channels.

The frequency of reading each channel should be adjustable so that trade offs
can be experimented with.

The following shall be fixed in software:

* power mode - full
* input pin to channel and setup and all related registers.

The users will use a command line program to control the ADC. It will have the
following features and options:

    voltmeter [options] [1][2]
    -h  --help          Display usage and all options.
    -o  --output-file   Write output to CSV file instead of stdout.

## Phase 2

There are requirements to monitor the following:

* monitoring speed using rotary encoders (digital input).
* monitoring temperatures using thermocouples.

The AD7124 can be used for all sorts of things from digital IO and even using
thermocouples so can probably be used for some or all of the above.

## Voltage converter

<https://bestengineeringprojects.com/9v-dc-to-plusminus-5v-dc-converter/>
<https://www.nutsvolts.com/magazine/article/dc-voltage-converter-circuits>

Figures 9, 11, 12 (best).

Alternatively use two USB plugtops, one to power the RPi as usual.  The other
is used with voltage regulators to provide two lots of 1.25V.

When I finally worked out what was needed, the second USB PSU was used to
provide a split rail supply to the ADC.  The internal reference was also used.

## References

<https://github.com/analogdevicesinc/arduino/tree/master/Arduino%20Uno%20R3/examples/CN0391_example>
<https://github.com/epsilonrt/ad7124>

