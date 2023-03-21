from state import State, SAMPLE_TIME
import time
import serial

def arduino_loop(state: State, port: str):
    arduino = serial.Serial(port=port, baudrate=115200, timeout=.1)
    while True:
        data = f"{state.left_speed} {state.right_speed}"
        time.sleep(SAMPLE_TIME)
        arduino.write(bytes(data, 'utf-8'))
        time.sleep(SAMPLE_TIME)
        data = arduino.readline()