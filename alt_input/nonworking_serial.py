import pygame
import usb.core
import usb.util

def handleJoyEvent(e):
    if e.type == pygame.JOYAXISMOTION:
        print("Axis", e.axis, "moved to", e.value)
    elif e.type == pygame.JOYBUTTONDOWN:
        print("Button", e.button, "pressed")
    elif e.type == pygame.JOYBUTTONUP:
        print("Button", e.button, "released")
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

def run_usb():
    pedals = usb.core.find(idVendor=0x06a3, idProduct=0x0763)
    joystick = usb.core.find(idVendor=0x06a3, idProduct=0x0bac)
    panel = usb.core.find(idVendor=0x06a3, idProduct=0x0d67) # check

    if None in (pedals, joystick, panel): # panel omitted for now
        raise ValueError('USB devices not found!')

    print(pedals)

    pedals.set_configuration()
    joystick.set_configuration()
    panel.set_configuration()

    while True:
        data = pedals.read(0x81, 8)
        print(data)

if __name__ == '__main__':
    run_usb()