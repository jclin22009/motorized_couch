import pygame
import time

motor_output = 0.0 # from -1.0 to 1.0, back to forward
steering = 0.0 # from -1.0 to 1.0, left to right
DRIFT_CORR = 0.0

def lower_bollards():
    print("Bollards lowering")

def handleJoyEvent(e):
    global motor_output, steering, DRIFT_CORR
    # axis 0: [-1,1] left to right
    # axis 1: [-1,1] up to down
    # axis 2: [-1,1] back left paddle forward to back
    # axis 3: [-1,1] back right paddle forward to back
    if e.type == pygame.JOYAXISMOTION:
        if e.axis == 0:
            steering = e.value
        elif e.axis == 1:
            if motor_output > 1.0:
                DRIFT_CORR -= motor_output - 1
                motor_output = 1.0
            elif motor_output < -1.0:
                DRIFT_CORR -= motor_output + 1
                motor_output = -1.0
            else:
                motor_output = (-e.value) + DRIFT_CORR
    # button 0: joystick back
    # button 1: joystick red
    # button 2: joystick big bottom button
    # button 3: joystick right button
    # button 4-11: swithces on bottom
    # button 12-13: red dial A and B
    elif e.type == pygame.JOYBUTTONDOWN:
        if e.button == 1:
            lower_bollards()
        if e.button == 4:
            DRIFT_CORR = -(motor_output - DRIFT_CORR)
            print("Recentering\n")

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
        print(f"Speed: {motor_output} Steering: {steering} Vertical Drift {DRIFT_CORR}", end = "\r")

if __name__ == '__main__':
    run_joystick()