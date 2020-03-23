# Implementation

A collection of notes that were written during development.

One thing you will notice as you look through the code is numerous commented
out print statements.  These were used during development and have been
intentionally left in the code in case they are needed again.

## Example code

The best place to start development is with working code.  So I tried to find
code that worked using the AD7124.

### Analog Devices Source Code

I started with the Analog Devices C driver example.

https://wiki.analog.com/resources/tools-software/uc-drivers/ad7124

Source code from here:
https://github.com/analogdevicesinc/no-OS/tree/master/drivers/adc/ad7124

Added this code to the repo.  Needed SPI and GPIO so found the
platform_drivers.c/h files and wrote a test program to drive it.  It worked
apart from the resulting app has SCLK and CE0 swapped.  Tried to figure out how
to fix this but it started getting deeply into Linux device trees, so I gave up
and tried PiGPIO instead.

## PiGPIO

Copied my test code over from my nRF905Py driver and hacked it to verify the
mode of operation.  Initially, tried to read the Id register as this was
recommended in the docs.  No response.  Tried to read an ADC register and it
came back with numbers.  Figured out that I wasn't setting a read bit when I was
trying to read the ID.  Fixed the code and it works.

One problem with this approach is that the PiGPIO code does not correctly
handle the DataReady signal that the ADC uses to say that data is ready for
reading.  The DataReady signal needs to be used correctly for the continuous
read mode.  In single read mode, the sampling rate is limited to about 8000
samples per second.

## ADC development

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

## Voltage converter

I had several attempts at working out what hardware was needed to measure
bipolar voltages correctly.  These are some links to things that I thought
would help.

<https://bestengineeringprojects.com/9v-dc-to-plusminus-5v-dc-converter/>
<https://www.nutsvolts.com/magazine/article/dc-voltage-converter-circuits>

Figures 9, 11, 12 (best).

Alternatively use two USB plugtops, one to power the RPi as usual.  The other
is used with voltage regulators to provide a split voltage supply.  This is
what I ended up using along with the internal reference.

## References

<https://github.com/analogdevicesinc/arduino/tree/master/Arduino%20Uno%20R3/examples/CN0391_example>
<https://github.com/epsilonrt/ad7124>

