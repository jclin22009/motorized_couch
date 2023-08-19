from threading import Thread
from joystick import Joystick
from motor_controller import MotorController

if __name__ == '__main__':
    # sudo pmset -a disablesleep 1
    joystick = Joystick()
    motor_controller = MotorController(joystick)
    t = Thread(target=motor_controller.start)
    t.start()
    joystick.start()
    motor_controller.stop()
    t.join()
    # sudo pmset -a disablesleep 0