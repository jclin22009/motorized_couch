# Default Configs

calibration_current: 10.0 (float)
current_control_bandwidth: 1000.0 (float)
current_lim: 10.0 (float)
direction: 0 (int32)
inverter_temp_limit_lower: 100.0 (float)
inverter_temp_limit_upper: 120.0 (float)
motor_type: 0 (uint8)
phase_inductance: 0.0 (float)
phase_resistance: 0.0 (float)
pole_pairs: 7 (int32)
pre_calibrated: False (bool)
requested_current_range: 60.0 (float)
resistance_calib_max_voltage: 2.0 (float)

# Commands

odrv0.config.enable_brake_resistor = False
odrv0.config.dc_max_negative_current = -3
odrv0.axis0.motor.config.calibration_current = 5
odrv0.axis0.motor.config.pole_pairs = 5
odrv0.axis0.motor.config.torque_constant = 8.27 / 120
odrv0.axis0.config.sensorless_ramp.current = 5
odrv0.axis0.controller.config.vel_limit = 50
odrv0.axis0.requested_state = AXIS_STATE_MOTOR_CALIBRATION
odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE
dump_errors(odrv0)
odrv0.axis0.controller.input_vel = 0
odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

# Based on VESC config

odrv0.axis0.controller.config.vel_gain = 0.004
odrv0.axis0.controller.config.vel_integrator_gain = 0.004
odrv0.axis0.controller.config.control_mode = 2
odrv0.axis0.sensorless_estimator.config.pm_flux_linkage = 0.01455
odrv0.save_configuration()
odrv0.reboot()

vel = (SPEED / 60) * 7 # turns/sec el
odrv0.axis0.config.sensorless_ramp.vel = vel
velocity = odrv0.axis0.config.sensorless_ramp.vel / 7 # turns/sec mech
odrv0.axis0.controller.config.vel_limit = 1.05 * velocity # 5% tolerance
odrv0.axis0.controller.input_vel = velocity

odrv0.axis0.controller.config.vel_gain = 0.01
odrv0.axis0.controller.config.vel_integrator_gain = 0.05
odrv0.axis0.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
odrv0.axis0.sensorless_estimator.config.pm_flux_linkage = 5.51328895422 / (7 * 270)
odrv0.axis0.motor.config.direction = 1

# Setup

odrv0.erase_configuration()

odrv0.config.brake_resistance = 4
odrv0.axis0.motor.config.motor_type = MotorType.HIGH_CURRENT
odrv0.axis0.config.sensorless_ramp.current = 1
odrv0.axis0.config.sensorless_ramp.ramp_time = 1
odrv0.axis0.motor.config.current_lim = 10
odrv0.axis0.motor.config.calibration_current = 5
odrv0.axis0.motor.config.pole_pairs = 9
odrv0.axis0.controller.config.vel_limit = 5
odrv0.axis0.controller.config.vel_gain = 0.01
odrv0.axis0.controller.config.vel_integrator_gain = 0.05
odrv0.axis0.controller.config.control_mode = ControlMode.VELOCITY_CONTROL
odrv0.axis0.config.enable_sensorless_mode = True
odrv0.axis0.sensorless_estimator.config.pm_flux_linkage = 0.002 # 83
odrv0.axis0.controller.config.input_mode = InputMode.VEL_RAMP
odrv0.save_configuration()

odrv0.axis0.requested_state = AXIS_STATE_MOTOR_CALIBRATION

odrv0.axis0.controller.input_vel = 0
odrv0.axis0.requested_state = AxisState.CLOSED_LOOP_CONTROL

dump_errors(odrv0)

odrv0.axis0.controller.input_vel = 0
odrv0.axis0.requested_state = AxisState.IDLE