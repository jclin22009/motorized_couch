import odrive
from odrive.enums import MotorType, ControlMode, InputMode, AxisState
import time
import fibre.libfibre

odrv0 = odrive.find_any()

SPEED = 1000 # rpm
RAMPTIME = 5 # sec

cnt = 0

callibrate = False

# if callibrate:
#     print(cnt,my_drive.axis0.current_state,
#     my_drive.axis0.sensorless_estimator.vel_estimate*60)
#     my_drive.axis0.motor.config.motor_type = MotorType.HIGH_CURRENT
#     my_drive.axis0.controller.config.vel_gain = 0.01
#     my_drive.axis0.controller.config.vel_integrator_gain = 0.05
#     my_drive.axis0.controller.config.control_mode = ControlMode.VELOCITY_CONTROL
#     my_drive.axis0.sensorless_estimator.config.pm_flux_linkage = 5.51328895422 / (7 * 270)

#     odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

#     velocity = SPEED / 60
#     accel = velocity / RAMPTIME
#     my_drive.axis0.config.sensorless_ramp.vel = velocity / 5 # trial

#     #ODrive | High performance motor control 2
#     print(cnt,my_drive.axis0.current_state,
#     my_drive.axis0.sensorless_estimator.vel_estimate*60)
#     my_drive.axis0.controller.config.vel_ramp_rate = accel
#     my_drive.axis0.controller.config.input_mode = InputMode.VEL_RAMP
#     my_drive.axis0.controller.input_vel = velocity

#     #Parameters & Commands | ODrive 3
#     print(cnt,my_drive.axis0.current_state,
#     my_drive.axis0.sensorless_estimator.vel_estimate*60)
#     my_drive.axis0.controller.config.vel_limit = 1.05 * velocity
#     my_drive.axis0.config.sensorless_ramp.current = 3
#     my_drive.axis0.motor.config.current_lim = 2.0 * my_drive.axis0.config.sensorless_ramp.current
#     # my_drive.axis0.motor.config.direction = 1

#     print(cnt,my_drive.axis0.current_state,
#     my_drive.axis0.sensorless_estimator.vel_estimate * 60)
#     my_drive.axis0.requested_state = 5 # AXIS_STATE_SENSORLESS_CONTROL
#     print(cnt,my_drive.axis0.current_state,
#     my_drive.axis0.sensorless_estimator.vel_estimate*60)

#     my_drive.save_configuration()

velocity = 3
pole_pairs = 10

# odrv0.axis0.requested_state = AxisState.IDLE

# try:
#     odrv0.erase_configuration()
# except fibre.libfibre.ObjectLostError:
#     pass # Saving configuration makes the device reboot

# print("Config complete.")

# time.sleep(3)

# print("Starting sensorless mode.")

# odrv0 = odrive.find_any()


# Pre Config
odrv0.axis0.motor.config.motor_type = MotorType.HIGH_CURRENT
odrv0.axis0.config.sensorless_ramp.current = 3
odrv0.axis0.controller.config.vel_gain = 0.01
odrv0.axis0.controller.config.vel_integrator_gain = 0.05
odrv0.axis0.controller.config.control_mode = ControlMode.VELOCITY_CONTROL
odrv0.axis0.controller.config.vel_limit = 1.05 * velocity # <a value greater than axis.config.sensorless_ramp.vel / (2pi * <pole_pairs>)>
odrv0.axis0.motor.config.current_lim = 2 * odrv0.axis0.config.sensorless_ramp.current
odrv0.axis0.sensorless_estimator.config.pm_flux_linkage = 5.51328895422 / (pole_pairs * 270) # 5.51328895422 / (<pole pairs> * <motor kv>)
odrv0.axis0.config.enable_sensorless_mode = True

accel = velocity / RAMPTIME
odrv0.axis0.config.sensorless_ramp.vel = velocity / 5 # trial
odrv0.axis0.controller.config.vel_ramp_rate = accel
odrv0.axis0.controller.config.input_mode = InputMode.VEL_RAMP

odrv0.axis0.controller.input_vel = velocity
odrv0.axis0.requested_state = AxisState.CLOSED_LOOP_CONTROL

try:
    odrv0.save_configuration()
except fibre.libfibre.ObjectLostError:
    pass # Saving configuration makes the device reboot

print("Config complete.")

time.sleep(3)

print("Starting sensorless mode.")

odrv0 = odrive.find_any()

odrv0.axis0.controller.input_vel = velocity
odrv0.axis0.requested_state = AxisState.CLOSED_LOOP_CONTROL

TIME_LIMIT = 10

while cnt < TIME_LIMIT:
    cnt = cnt + 1
    time.sleep(0.5)
    print(cnt,odrv0.axis0.current_state,
    odrv0.axis0.sensorless_estimator.vel_estimate*60)

odrv0.axis0.requested_state = AxisState.IDLE