import pygame
import math

class Axis:
    STEERING = 0
    THROTTLE = 1

class Button:
    TRIGGER = 0
    RED_BUTTON = 1
    CENTER_BUTTON = 2
    BLACK_BUTTON = 3
    T1 = 4
    T2 = 5
    T3 = 6
    T4 = 7
    T5 = 8
    T6 = 9
    T7 = 10
    T8 = 11
    MODE_A = 12
    MODE_B = 13

# arduino_dev = '/dev/cu.usbmodem1301'
# arduino = serial.Serial(port=arduino_dev, baudrate=9600)

DEADZONE = 0.1
MAX = 1.0
SLOW_SPEED = 25
MEDIUM_SPEED = 50
FAST_SPEED = 100
TURN_DAMPING = 3

class Joystick:
    max_speed = SLOW_SPEED
    steering = 0
    throttle = 0
    left_speed = 0
    right_speed = 0

    def update_speed(self):
        # https://robotics.stackexchange.com/a/20626
        joy_x = self.steering
        joy_y = self.throttle
        epsilon = 1e-5 # to avoid division by zero
        # convert to polar coordinates
        theta = math.atan2(joy_y, joy_x)
        r = math.sqrt(joy_x * joy_x + joy_y * joy_y)
        # this is the maximum r for a given angle
        if abs(joy_x) > abs(joy_y):
            max_r = abs(r / joy_x) if joy_x != 0 else 0
        else:
            max_r = abs(r / joy_y) if joy_y != 0 else 0
        # this is the actual throttle
        magnitude = r / max_r if max_r != 0 else 0
        left_relative_speed = magnitude * (math.sin(theta) + math.cos(theta) / TURN_DAMPING)
        right_relative_speed = magnitude * (math.sin(theta) - math.cos(theta) / TURN_DAMPING)
        self.left_speed = left_relative_speed * self.max_speed
        self.right_speed = right_relative_speed * self.max_speed

    def __init__(self):
        pygame.init()
        pygame.joystick.init()
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()

    def scale_value(self, input):
        sign = 1
        if (input < 0.0):
            sign = -1
            input = -input

        if (input > 1.0):
            input = 1.0
        
        area = MAX - DEADZONE
        margin = input - DEADZONE
        return (margin / area) * sign

    # Helper function for handling the motion
    def handle_motion(self, e):
        if e.value > 0:
            if e.value > DEADZONE:
                return self.scale_value(e.value)
            else:
                return 0.0
        else:
            if e.value < -DEADZONE:
                return self.scale_value(e.value)
            else:
                return 0.0

    def handle_event(self, e):
        if e.type == pygame.JOYAXISMOTION:
            if e.axis == Axis.STEERING:
                self.steering = self.handle_motion(e)
            elif e.axis == Axis.THROTTLE:
                self.throttle = -self.handle_motion(e)
        elif e.type == pygame.JOYBUTTONDOWN:
            if e.button == Button.RED_BUTTON:
                return True # Stop running
            elif e.button == Button.BLACK_BUTTON:
                # arduino.write(bytes("\n", 'utf-8'))
                pass
            elif e.button == Button.MODE_A: # Mode A
                self.max_speed = MEDIUM_SPEED
            elif e.button == Button.MODE_B: # Mode B
                self.max_speed = FAST_SPEED

        elif e.type == pygame.JOYBUTTONUP:
            if e.button == 12 or e.button == 13:
                self.max_speed = SLOW_SPEED

        # hats follow the ([-1,1], [-1,1]) coordinates you expect
        elif e.type == pygame.JOYHATMOTION:
            print("Hat", e.hat, "moved to", e.value)

    def start(self):
        while True:
            e = pygame.event.wait()
            if e.type == pygame.QUIT:
                break
            if self.handle_event(e):
                break
            self.update_speed()
            # print("Steering: ", self.steering, "Throttle: ", self.throttle, "Left: ", self.left_speed, "Right: ", self.right_speed)

if __name__ == '__main__':
    Joystick().start()