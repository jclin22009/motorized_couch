from simple_pid import PID
import time
import numpy as np
from state import State, SAMPLE_TIME

MAX_SPEED = 60
DESIRED_DEPTH = 1
steering_pid = PID(-80, 0, -40, setpoint=0)
speed_pid = PID(-40, 0, -25, setpoint=0)

steering_pid.sample_time = SAMPLE_TIME
speed_pid.sample_time = SAMPLE_TIME

steering_pid.output_limits = (-MAX_SPEED * 2/3, MAX_SPEED * 2/3)
speed_pid.output_limits = (0, MAX_SPEED * 1/3)

def pid_loop(state: State):
    while True:
        if state.stopped:
            steering_pid.auto_mode = False
            speed_pid.auto_mode = False
            state.left_speed = 0
            state.right_speed = 0
        else:
            steering_pid.auto_mode = True
            speed_pid.auto_mode = True
            steering = steering_pid(state.theta)
            speed = speed_pid(state.z - DESIRED_DEPTH)
            state.left_speed = int(speed + max(0, steering))
            state.right_speed = int(speed - min(0, steering))
        
        print(state)
        time.sleep(SAMPLE_TIME)