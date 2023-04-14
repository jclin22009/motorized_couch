from pyvesc import VESC
import time

# serial port that VESC is connected to. Something like "COM3" for windows and as below for linux/mac
left_serial_port = '/dev/cu.usbmodem3'
right_serial_port = '/dev/cu.usbmodem3011'

# a function to show how to use the class as a static object.
def run_motor_as_object():
    left_motor = VESC(serial_port=left_serial_port)
    right_motor = VESC(serial_port=right_serial_port)
    print("Left firmware: ", left_motor.get_firmware_version())
    print("Right firmware: ", right_motor.get_firmware_version())

    # sweep servo through full range
    for i in range(0, 500):
        time.sleep(0.01)
        left_motor.set_rpm(10 * i)
        right_motor.set_rpm(10 * i)

    # IMPORTANT: YOU MUST STOP THE HEARTBEAT IF IT IS RUNNING BEFORE IT GOES OUT OF SCOPE. Otherwise, it will not
    #            clean-up properly.
    left_motor.stop_heartbeat()
    right_motor.stop_heartbeat()


if __name__ == '__main__':
    run_motor_as_object()