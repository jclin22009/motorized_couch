import pyvesc
from pyvesc.VESC.messages import SetRPM
import time

can_id = 78
vesc = pyvesc.VESC(serial_port="/dev/tty.usbmodem3041")

def set_rpm(rpm):
    packet = pyvesc.encode(SetRPM(rpm,can_id=can_id))
    print(packet)
    vesc.write(packet)

set_rpm(1000)
time.sleep(2)
set_rpm(0)

# \x02\x07!M\x08\x00\x00\x04\x1a\x8fV\x03
# \x02\x07!N\x08\x00\x00\x03\xe8\x17|\x03

# \x02\x07"N\x08\x00\x00\x03\xe8\xcf\xfe\x03

# \x02\x07\x22\x4d\x05\x00\x00\x27\x10\x84\x51\x03