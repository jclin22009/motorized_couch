import pygame
import time
import serial
from threading import Thread

arduino = serial.Serial(port='/dev/tty.usbserial-DB00JLKU', baudrate=115200, timeout=.1)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

motor_output = 0.0 # from -1.0 to 1.0, back to forward
steering = 0.0 # from -1.0 to 1.0, left to right
DEADZONE = 0.1
MAX = 1.0

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
    global motor_output, steering
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

    elif e.type == pygame.JOYBUTTONUP:
        pass

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
        left_speed = int(70 * max(motor_output + steering, 0))
        right_speed = int(70 * max(motor_output - steering, 0))
        # average_speed = 50 * motor_output
        # scaled_steering = 20 * steering
        # left_speed = int(max(average_speed + scaled_steering, 0))
        # right_speed = int(max(average_speed - scaled_steering, 0))
        print(f"Left: {left_speed} Right: {right_speed} Speed: {motor_output} Steering: {steering}")
        value = write_read(f"{left_speed} {right_speed}")
        print(value.strip())

if __name__ == '__main__':
    t = Thread(target=update_arduino)
    t.start()
    run_joystick()