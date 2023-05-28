from __future__ import print_function, division

import odrive
from odrive.enums import *
import time
import math
import numpy as np
import readchar
import sys
testing = False # testing variable
command = ["Stopped", 0]
incrament = 0.5


config = {
	"wheel_radius" : 0.1,
	"drive_gearing" : 28.55, # 64 means a gearing of 64 to one
	"flipper_gearing" : 81.37
}

serial_list_raw = ["2065358F524B"]

odrv = None


############################################
#### CALIBRATION PROCESS ###################
############################################


# Calibrate one odrive 
# Input: Serial id of the odrive as a string
# Output: ODrive object
def full_reset_and_calibrate(targetID, i=0):
	# """Completely resets the Odrive, calibrates axis0 and configures axis0 to only encoder index search on startup and be ready in AXIS_STATE_CLOSED_LOOP_CONTROL"""
	# print("------------- CALIBRATION ODRV " + str(i) + " -------------\n")
	# print("Searching for Serial number: " + targetID)
	# odrv0 = odrive.find_any(serial_number=targetID)

	# odrv0.erase_configuration()
	# print("ODRV NO." + str(i) + "  " + "Erased [1/7]")
	# try: # Reboot causes loss of connection, use try to supress errors
	# 	odrv0.reboot()
	# except:
	# 	pass
	print("ODRV NO." + str(i) + "  " + "Rebooted [2/7]")
	odrv0 = odrive.find_any(serial_number = targetID) # Reconnect to the Odrive
	print("ODRV NO." + str(i) + "  " + "Connected [3/7]")
	odrv0.axis0.motor.config.pre_calibrated = True # Set all the flags required for pre calibration
	odrv0.axis0.encoder.config.pre_calibrated = True
	odrv0.axis0.encoder.config.use_index = True
	odrv0.axis0.config.startup_encoder_index_search = True # Change startup sequence
	odrv0.axis0.config.startup_closed_loop_control = True
	odrv0.axis0.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE # Calibrate
	print("ODRV NO." + str(i) + "  " + "Started calibration 1 [4/7]", end="")
	while odrv0.axis0.current_state != AXIS_STATE_IDLE: # Wait for calibration to be done
		time.sleep(0.1)
		print(".", end="")
	odrv0.save_configuration()

	print("\nODRV NO." + str(i) + "  " + "AXIS 1. Calibration complete [5/7]\n")
	print("now will begin calibration sequence for second axis for ODRV NO." + str(i))
	time.sleep(3)
	odrv0.axis1.motor.config.pre_calibrated = True # Set all the flags required for pre calibration
	odrv0.axis1.encoder.config.pre_calibrated = True
	odrv0.axis1.encoder.config.use_index = True
	odrv0.axis1.config.startup_encoder_index_search = True # Change startup sequence
	odrv0.axis1.config.startup_closed_loop_control = True
	odrv0.axis1.requested_state = AXIS_STATE_FULL_CALIBRATION_SEQUENCE # Calibrate
	print("ODRV NO." + str(i) + "  " + "Started calibration 2 [6/7]", end="")
	while odrv0.axis1.current_state != AXIS_STATE_IDLE: # Wait for calibration to be done
		time.sleep(0.5)
		print(".", end="")

	print("\nODRV NO." + str(i) + "  " + "AXIS 2. Calibration 2 complete [7/7]")

	#closed loop control for both axis
	odrv0.save_configuration()
	odrv0.axis0.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
	odrv0.axis1.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL

	return odrv0

# Calibrate all odrives. 
# Input: Serial ids of the odrives as a list of strings
# Output: List of all ODrive objects
def calibrateODrives(serialIDs):
	odrives = []
	for i, ID in enumerate(serialIDs):
		odrives.append(full_reset_and_calibrate(ID, i+1))

	return odrives

def obtainODriveObjects(serialIDs):
	print("No calibration Mode")
	odrives = []
	for i, ID in enumerate(serialIDs):
		print("Searching for ODrive with id = " + ID)
		odrives.append(odrive.find_any(serial_number=ID))
		print("Found an ODrive")

	return odrives




############################################
#### ODRIVE CONTROL COMMANDS ###############
############################################


# Set rps of the output shaft
# Input: axis as ODrive object, desired rps of the output, gear ratio of output to motor
def set_rps(axis, rps, gear_ratio):
	axis.requested_state = AXIS_STATE_CLOSED_LOOP_CONTROL
	axis.controller.config.control_mode = CONTROL_MODE_VELOCITY_CONTROL
	axis.controller.input_vel = rps * 2 * math.pi * gear_ratio * 8192

# Set current of a particular axis
# Input: axis as ODrive object, max current through that axis
def set_current_limit(axis, current_limit):
	axis.motor.config.current_lim = current_limit


# Set current of a particular axis
# Input: axis as ODrive object, max current through that axis
def set_velocity_limit(axis, velocity_limit):
	axis.controller.config.vel_limit = velocity_limit




############################################
#### PROGRAM NAVIGATION ####################
############################################

def initial_setting(debug = False):
	global odrv

	if not debug:
		print("-------------- ODRIVE SANITY CHECK --------------\n\n")
		print("Full Reset and Calibrate? (y/n)")

		while 1:
			value = input()
			if value == 'y':
				odrv = calibrateODrives(serial_list_raw)
				break
			elif value == 'n':
				odrv = obtainODriveObjects(serial_list_raw)
				break
			else:
				print("Enter either y or n to continue")

def control_loop(debug = False):
	global odrv
	
	print("Control Loop: Press Enter to Begin")
	input()

	previous = 0
	speed = 0
	incrament = 0.02
	threshold = incrament * 10


	max_velocity = 500000

	if not debug:
		set_velocity_limit(odrv[0].axis0, max_velocity)
		set_velocity_limit(odrv[0].axis1, max_velocity)

		rightTrack = odrv[0].axis1
		leftTrack = odrv[0].axis0

	mode = 0

	select = ["Move FWD", "Move Left Track", "Move Right Track", "Move Front Flipper", "Move Rear Flipper"]
	while 1:

	

		input_val = readchar.readchar()

		if input_val == "1":
			mode = 1
			print("--  MODE : " + select[mode - 1])
		elif input_val == "2":
			mode = 2
			print("--  MODE : " + select[mode - 1])
		elif input_val == "3":
			mode = 3
			print("--  MODE : " + select[mode - 1])
		elif input_val == "4":
			mode = 4
			print("--  MODE : " + select[mode - 1])
		elif input_val == "5":
			mode = 5
			print("--  MODE : " + select[mode - 1])

		elif input_val == "w":
			speed += incrament
			print("speed INCREASE")
		elif input_val == "s":
			speed -= incrament
			print("speed DECREASE")
		elif input_val == "0":
			speed = 0
			print("speed ZERO")
		elif input_val == "q":
			break
		else:
			print("No command parsed")


		current = speed

		if current < 0:
			current = 0
		
		if abs(previous - current) > threshold:
			current = previous + np.sign(current - previous)*threshold
			
		if not debug:

			if mode == 1:
				set_rps(rightTrack, -1* current, config['drive_gearing'])
				set_rps(leftTrack, current, config['drive_gearing'])

			elif mode == 2:
				set_rps(rightTrack, current, config['drive_gearing'])
				set_rps(leftTrack, 0, config['drive_gearing'])

			elif mode == 3:
				set_rps(rightTrack, 0, config['drive_gearing'])
				set_rps(leftTrack, current, config['drive_gearing'])

			elif mode == 4:
				set_rps(rightTrack, 0, config['drive_gearing'])
				set_rps(leftTrack, 0, config['drive_gearing'])

			elif mode == 5:
				set_rps(rightTrack, 0, config['drive_gearing'])
				set_rps(leftTrack, 0, config['drive_gearing'])

		print("speed is: " + str(current))

		previous = current



# MAIN PROGRAM 
def main():
	initial_setting(debug = False)
	control_loop(debug = False)

if __name__ == "__main__":
	main()

