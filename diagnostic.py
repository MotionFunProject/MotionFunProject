# Motion Fun Project
#
# A Simple Sensor Test to make sure everything is functioning properly.
# Will print the heading, roll, and pitch continuously to the console. 
#
# See BNO055_Commands.txt for a list of all the available commands.

import logging
import sys
import time

# Import our library to make life super easy 
from Adafruit_BNO055 import BNO055

# Raspberry Pi configuration with serial UART and RST connected to GPIO 18:
bno = BNO055.BNO055(serial_port='/dev/ttyAMA0', rst=18)

# Verbose Debugging with -v 
if len(sys.argv) == 2 and sys.argv[1].lower() == '-v':
    logging.basicConfig(level=logging.DEBUG)

# Initialize the BNO055 and stop if undetected. 
if not bno.begin():
    raise RuntimeError('The sensor is not detected. Make sure the sensor is connected to your Pi')


def systemstatus():
    # Print system status and self test result.
    status, self_test, error = bno.get_system_status()
    print('System status: {0}'.format(status))
    print('Self test result (0x0F is normal): 0x{0:02X}'.format(self_test))
    # Print out an error if system status is in error mode.
    if status == 0x01:
        print('System error: {0}'.format(error))

def diagnostictool():
    # Print BNO055 software revision and other diagnostic data.
    sw, bl, accel, mag, gyro = bno.get_revision()
    print('Software version:   {0}'.format(sw))
    print('Bootloader version: {0}'.format(bl))
    print('Accelerometer ID:   0x{0:02X}'.format(accel))
    print('Magnetometer ID:    0x{0:02X}'.format(mag))
    print('Gyroscope ID:       0x{0:02X}\n'.format(gyro))

def simpleTest():
    # Will Print head, pitch, and roll continuously 
    print('Reading sensor data, press Ctrl-C to quit...')
    while True:
        # Read the Euler angles.
        heading, roll, pitch = bno.read_euler()
        # Read the calibration status.
        sys, gyro, accel, mag = bno.get_calibration_status()
        # Print everything out.
        print('Heading={0:0.2F} Roll={1:0.2F} Pitch={2:0.2F}\tSys_cal={3} Gyro_cal={4} Accel_cal={5} Mag_cal={6}'.format(
              heading, roll, pitch, sys, gyro, accel, mag))
        time.sleep(1)

systemstatus()
diagnostictool()
simpleTest()

   

