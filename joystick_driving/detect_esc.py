import sys
import glob
import serial
from pyvesc import VESC
from can_vesc import CanVESC
import time

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

def connect_escs():
    left_vesc_id = 42
    right_can_id = 78
    left_vesc = None
    while left_vesc is None:
        for port in serial_ports():
            if port.startswith("/dev/tty.usbmodem"):
                print(f"Connecting to {port}")
                try:
                    vesc = VESC(serial_port=port)
                    byte = vesc.get_measurements().__dict__['app_controller_id']
                    vesc_id = int.from_bytes(byte, byteorder='big', signed=True)
                    if vesc_id == left_vesc_id:
                        left_vesc = vesc
                except:
                    print("Error connecting to VESC, retrying")
        print("No VESCs found, retrying")
        time.sleep(1)
    right_vesc = CanVESC(parent_vesc=left_vesc, can_id=right_can_id)
    return left_vesc, right_vesc