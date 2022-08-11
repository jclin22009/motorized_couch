import hid # https://github.com/libusb/hidapi
import pygame
import time

POLLING_RATE_SEC = 0.1

def print_all_devices():
    for device in hid.enumerate():
        print(f"0x{device['vendor_id']:04x}:0x{device['product_id']:04x} {device['product_string']}")

def config_devices():
    pedals = hid.device()
    pedals.open(0x06a3, 0x0763)
    joystick = hid.device()
    joystick.open(0x06a3, 0x0bac)
    panel = hid.device()
    panel.open(0x06a3, 0x0d67)

    if None in (pedals, joystick, panel):
        raise ValueError('USB devices not found!')
    
    return pedals, joystick, panel

def handleJoyEvent(e):
    if e.type == pygame.JOYAXISMOTION:
        print("Axis", e.axis, "moved to", e.value)
    elif e.type == pygame.JOYBUTTONDOWN:
        print("Button", e.button, "pressed")
    elif e.type == pygame.JOYBUTTONUP:
        print("Button", e.button, "released")
    elif e.type == pygame.JOYHATMOTION:
        print("Hat", e.hat, "moved to", e.value)


def read_left_pedal(pedals):
    '''
    Read the left pedal intensity. 0-127'''
    return pedals.read(3)[0]

def read_joystick(joystick):
    '''
    Read the joystick position. -1 to 1'''
    # pygame.event.pump()
    # return joystick.get_axis(0)
    for event in pygame.event.get():
        if event.type == pygame.JOYAXISMOTION:
            return event.value
        if event.type == pygame.QUIT:
            pygame.quit()

def master_switches_on(panel, previous_panel_state):
    '''
    Read the master switches state. 0=off, 1=on'''
    return 1

def set_motor_power(power):
    pass

def set_steering(steering):
    pass

'''
switch panel data 

comes in format (x,y,z) representing all values
numbers overflow TO THE RIGHT

flipping switches on ADDS, flipping switch off SUBTRACTS

INPUTS:
the flippy switches add 2^(their position left to right, top to bottom, starting from 0)


'''

def main():
    # print_all_devices()
    pygame.init()
    pygame.joystick.init()
    # joystick = pygame.joystick.Joystick(0)
    # # pedals, joystick_fake, panel = config_devices()


    while True:
        pygame.event.pump() #allow Pygame to handle internal actions
        joystick_count = pygame.joystick.get_count()

        for i in range(joystick_count):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()

            name = joystick.get_name()
            axes = joystick.get_numaxes()
            hats = joystick.get_numhats()
            button = joystick.get_numbuttons()

            joy = joystick.get_axis(0)

            print(name, joy)
    # while True:
        # if not master_switches_on(panel, prev_state):
        #     print('Master switches are off. Please boot to takeoff!')
        #     time.sleep(1)
        #     continue

        # motor_power = read_left_pedal(pedals)
        # steering = read_joystick(joystick)
        # print(motor_power)

        # set_motor_power(motor_power)
        # set_steering(steering)
        # print(read_left_pedal(pedals))
        # print(read_joystick(joystick))
        # print(panel.read(3))



        # sleep(POLLING_RATE_SEC)

if __name__ == '__main__':
    main()