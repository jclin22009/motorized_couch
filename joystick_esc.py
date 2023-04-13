import pygame
from pyvesc import VESC
from threading import Thread
import numpy as np

left_esc = '/dev/cu.usbmodem3'
right_esc = '/dev/cu.usbmodem3011'
left_motor = VESC(serial_port=left_esc)
right_motor = VESC(serial_port=right_esc)

motor_output = 0.0 # from -1.0 to 1.0, back to forward
steering = 0.0 # from -1.0 to 1.0, left to right
DEADZONE = 0.1
MAX = 1.0

SLOW_SPEED = 25
MEDIUM_SPEED = 50
FAST_SPEED = 100
max_speed = SLOW_SPEED

def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

def lower_bollards():
    print("Bollards lowering")

# Helper function for handling the motion
def handleMotion(e):
    if e.value > 0:
        if e.value > DEADZONE:
            return calcScaledValue(e.value)
        else:
            return 0.0
    else:
        if e.value < -DEADZONE:
            return calcScaledValue(e.value)
        else:
            return 0.0

# Given the offset for DEADZONE and our limit of MAX_STEERING, returns the value we should get
def calcScaledValue(input):
    sign = 1
    if (input < 0.0):
        sign = -1
        input = -input

    if (input > 1.0):
        input = 1.0
    
    area = MAX - DEADZONE
    margin = input - DEADZONE
    return (margin / area) * sign

def handleJoyEvent(e):
    global max_speed, motor_output, steering
    # axis 0: [-1,1] left to right
    # axis 1: [-1,1] up to down
    # axis 2: [-1,1] back left paddle forward to back
    # axis 3: [-1,1] back right paddle forward to back
    if e.type == pygame.JOYAXISMOTION:
        if e.axis == 0:
            steering = handleMotion(e)
        elif e.axis == 1:
            motor_output = -handleMotion(e)
    # button 0: joystick back
    # button 1: joystick red
    # button 2: joystick big bottom button
    # button 3: joystick right button
    # button 4-11: swithces on bottom
    # button 12-13: red dial A and B
    elif e.type == pygame.JOYBUTTONDOWN:
        if e.button == 1:
            lower_bollards()
        elif e.button == 12: # Mode A
            max_speed = MEDIUM_SPEED
        elif e.button == 13: # Mode B
            max_speed = FAST_SPEED

    elif e.type == pygame.JOYBUTTONUP:
        if e.button == 12 or e.button == 13:
            max_speed = SLOW_SPEED

    # hats follow the ([-1,1], [-1,1]) coordinates you expect
    elif e.type == pygame.JOYHATMOTION:
        print("Hat", e.hat, "moved to", e.value)
    

def run_joystick():
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    while True:
        e = pygame.event.wait()
        if e.type == pygame.QUIT:
            break
        handleJoyEvent(e)

def update_arduino():
    while True:
        # 50 for one person
        left_speed = int(max_speed * (motor_output + (1 - 0.8 * motor_output) * steering))
        right_speed = int(max_speed * (motor_output - (1 -  0.8 * motor_output) * steering))
        # average_speed = 50 * motor_output
        # scaled_steering = 20 * steering
        # left_speed = int(max(average_speed + scaled_steering, 0))
        # right_speed = int(max(average_speed - scaled_steering, 0))
        print(f"Left: {left_speed} Right: {right_speed} Speed: {motor_output} Steering: {steering}")
        abs_left_speed = abs(left_speed)
        abs_right_speed = abs(right_speed)
        left_rpm = 0 if abs_left_speed < 10 else map_range(abs_left_speed, 0, 100, 3000, 8000)
        right_rpm = 0 if abs_right_speed < 10 else map_range(abs_right_speed, 0, 100, 3000, 8000)
        left_motor.set_rpm(-np.sign(left_speed) * left_rpm)
        right_motor.set_rpm(np.sign(right_speed) * right_rpm)

if __name__ == '__main__':
    # sudo pmset -a disablesleep 1
    t = Thread(target=update_arduino)
    t.start()
    run_joystick()
    # sudo pmset -a disablesleep 0