from simple_pid import PID
import time
from state import State, SAMPLE_TIME

MAX_SPEED = 60
DESIRED_DEPTH = 1
# steering_pid = PID(-30, 0, -60, setpoint=0)
# speed_pid = PID(-30, 0, -60, setpoint=0)
steering_pid = PID(-40, 0, -60, setpoint=0)
speed_pid = PID(-10, 0, -30, setpoint=0)

steering_pid.sample_time = SAMPLE_TIME
speed_pid.sample_time = SAMPLE_TIME

# steering_pid.output_limits = (-MAX_SPEED, MAX_SPEED * 1/2)
# speed_pid.output_limits = (0, MAX_SPEED * 2/3)
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
            left_speed = max(int(speed + steering), 0)
            right_speed = max(int(speed - steering), 0)
            state.left_speed = left_speed
            state.right_speed = right_speed
        
        print(state)
        time.sleep(SAMPLE_TIME)