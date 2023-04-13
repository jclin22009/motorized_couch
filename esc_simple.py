from pyvesc import VESC
import time

# serial port that VESC is connected to. Something like "COM3" for windows and as below for linux/mac
serial_port = '/dev/cu.usbmodem3'

# a function to show how to use the class as a static object.
def run_motor_as_object():
    motor = VESC(serial_port=serial_port)
    print("Firmware: ", motor.get_firmware_version())

    # sweep servo through full range
    for i in range(300, 800):
        time.sleep(0.01)
        motor.set_rpm(10 * i)

    # IMPORTANT: YOU MUST STOP THE HEARTBEAT IF IT IS RUNNING BEFORE IT GOES OUT OF SCOPE. Otherwise, it will not
    #            clean-up properly.
    motor.stop_heartbeat()


if __name__ == '__main__':
    run_motor_as_object()