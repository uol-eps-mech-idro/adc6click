# Performs loopback test using PiGPIO.
# Connect pins 19 (SPI0 MOSI) and 21 (SPI0 MISO).

if [ ! -e /var/run/pigpio.pid ]
then
  sudo pigpiod
  echo $?
fi
pigs spio 0 50000 0
echo $?
echo "Expected response is 6 23 45 67 89 12 13"
pigs spix 0 23 45 67 89 12 13
echo $?
echo "Done"
