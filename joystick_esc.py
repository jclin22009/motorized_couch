import pygame
from pyvesc import VESC
from threading import Thread
import numpy as np
# import serial

right_motor_dev = '/dev/cu.usbmodem3041'
left_motor_dev = '/dev/cu.usbmodem4'
# arduino_dev = '/dev/cu.usbmodem1301'

left_motor = VESC(serial_port=left_motor_dev)
right_motor = VESC(serial_port=right_motor_dev)
# arduino = serial.Serial(port=arduino_dev, baudrate=9600)

steering = 0
motor_output = 0
DEADZONE = 0.1
MAX = 1.0

SLOW_SPEED = 25
MEDIUM_SPEED = 50
FAST_SPEED = 100
max_speed = SLOW_SPEED

braking = False

def map_range(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

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
    global steering, motor_output, max_speed, braking
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
            return True # Stop running
        elif e.button == 2:
            braking = True
        elif e.button == 3:
            # arduino.write(bytes("\n", 'utf-8'))
            pass
        elif e.button == 12: # Mode A
            max_speed = MEDIUM_SPEED
        elif e.button == 13: # Mode B
            max_speed = FAST_SPEED

    elif e.type == pygame.JOYBUTTONUP:
        if e.button == 2 or e.button == 3:
            braking = False
        elif e.button == 12 or e.button == 13:
            max_speed = SLOW_SPEED

    # hats follow the ([-1,1], [-1,1]) coordinates you expect
    elif e.type == pygame.JOYHATMOTION:
        print("Hat", e.hat, "moved to", e.value)

left_rpm = 0
right_rpm = 0

def handle_motion():
    global left_rpm, right_rpm
    if braking:
        target_left_rpm = 0
        target_right_rpm = 0
    else:
        left_speed = int(max_speed * (motor_output + (1 - 0.8 * motor_output) * 0.5 * steering))
        right_speed = int(max_speed * (motor_output - (1 -  0.8 * motor_output) * 0.5 * steering))
        abs_left_speed = abs(left_speed)
        abs_right_speed = abs(right_speed)
        abs_left_rpm = 0 if abs_left_speed < 5 else map_range(abs_left_speed, 0, 100, 0, 10000)
        abs_right_rpm = 0 if abs_right_speed < 5 else map_range(abs_right_speed, 0, 100, 0, 10000)
        target_left_rpm = np.sign(left_speed) * abs_left_rpm
        target_right_rpm = np.sign(right_speed) * abs_right_rpm
        target_left_rpm = max(0, target_left_rpm)
        target_right_rpm = max(0, target_right_rpm)
        print(f"Left: {left_speed}/{target_left_rpm} Right: {right_speed}/{target_right_rpm} Speed: {motor_output} Steering: {steering}")
    
    # left_rpm += 0.001 * (target_left_rpm - left_rpm)
    # right_rpm += 0.001 * (target_right_rpm - right_rpm)
    # left_motor.set_rpm(int(left_rpm))
    # right_motor.set_rpm(int(right_rpm))
    left_motor.set_rpm(int(target_left_rpm))
    right_motor.set_rpm(int(target_right_rpm))
    # left_motor.set_current(int(target_left_rpm))
    # right_motor.set_current(int(target_right_rpm))


def run_joystick():
    pygame.init()
    pygame.joystick.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    while True:
        e = pygame.event.wait()
        if e.type == pygame.QUIT:
            break
        if handleJoyEvent(e):
            break
        
def update_motion():
    while not stop_thread:
        handle_motion()

if __name__ == '__main__':
    # sudo pmset -a disablesleep 1
    stop_thread = False
    t = Thread(target=update_motion)
    t.start()
    run_joystick()
    stop_thread = True
    t.join()
    left_motor.stop_heartbeat()
    right_motor.stop_heartbeat()
    # sudo pmset -a disablesleep 0