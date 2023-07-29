import sys
import glob
import serial
from pyvesc import VESC

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
    left_id = 47
    right_id = 56
    left_vesc = None
    right_vesc = None
    while left_vesc is None or right_vesc is None:
        for port in serial_ports():
            if port.startswith("/dev/tty.usbmodem"):
                print(f"Connecting to {port}")
                try:
                    vesc = VESC(serial_port=port)
                    byte = vesc.get_measurements().__dict__['app_controller_id']
                    vesc_id = int.from_bytes(byte, byteorder='big', signed=True)
                    if vesc_id == left_id:
                        left_vesc = vesc
                    elif vesc_id == right_id:
                        right_vesc = vesc
                except:
                    print("Error connecting to VESC, retrying")
    return left_vesc, right_vesc