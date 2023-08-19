import numpy as np
from detect_esc import connect_escs
from utils import map_range
from joystick import Joystick

# arduino_dev = '/dev/cu.usbmodem1301'
# arduino = serial.Serial(port=arduino_dev, baudrate=9600)

MIN_RPM = 400

class MotorController:
    joystick: Joystick

    is_stopped = False
    stop_thread = False

    def __init__(self, joystick: Joystick) -> None:
        self.joystick = joystick

    def handle_motion(self):
        try:
            if self.is_stopped and self.left_motor.get_rpm() >= MIN_RPM or self.right_motor.get_rpm() >= MIN_RPM:
                print("Starting")
                self.is_stopped = False
            elif not self.is_stopped and self.left_motor.get_rpm() < MIN_RPM and self.right_motor.get_rpm() < MIN_RPM:
                print("stopping")
                self.is_stopped = True
        except:
            pass

        if self.is_stopped:
            return

        left_speed = self.joystick.left_speed
        right_speed = self.joystick.right_speed
        abs_left_speed = abs(left_speed)
        abs_right_speed = abs(right_speed)
        abs_left_rpm = 0 if abs_left_speed < 5 else map_range(abs_left_speed, 0, 100, 0, 10000)
        abs_right_rpm = 0 if abs_right_speed < 5 else map_range(abs_right_speed, 0, 100, 0, 10000)
        target_left_rpm = np.sign(left_speed) * abs_left_rpm
        target_right_rpm = np.sign(right_speed) * abs_right_rpm
        target_left_rpm = max(0, target_left_rpm)
        target_right_rpm = max(0, target_right_rpm)
        print(f"Left: {left_speed}/{target_left_rpm} Right: {right_speed}/{target_right_rpm}")
        self.left_motor.set_rpm(int(target_left_rpm))
        self.right_motor.set_rpm(int(target_right_rpm))
        
    def start(self):
        self.left_motor, self.right_motor = connect_escs()
        while not self.stop_thread:
            self.handle_motion()
        self.left_motor.stop_heartbeat()
        self.right_motor.stop_heartbeat()

    def stop(self):
        self.stop_thread = True