from __future__ import print_function

import odrive
import time
import math

# Find a connected ODrive (this will block until you connect one)
my_drive = odrive.find_any()

# Find an ODrive that is connected on the serial port /dev/ttyUSB0
#my_drive = odrive.find_any("serial:/dev/ttyUSB0")

# To read a value, simply read the property
print("Bus voltage is " + str(my_drive.vbus_voltage) + "V")

# Or to change a value, just assign to the property
my_drive.axis0.controller.input_pos = 3.14
print("Position setpoint is " + str(my_drive.axis0.controller.pos_setpoint))

# And this is how function calls are done:
my_drive.axis0.controller.pos_setpoint(0.0, 0.0, 0.0)

# A sine wave to test
t0 = time.monotonic()
while True:
    setpoint = 10000.0 * math.sin((time.monotonic() - t0)*2)
    print("goto " + str(int(setpoint)))
    my_drive.axis0.controller.pos_setpoint(setpoint, 0.0, 0.0)
    time.sleep(0.01)