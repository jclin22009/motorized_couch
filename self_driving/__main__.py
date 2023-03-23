import threading
from state import State
from shirt import track_shirt
from pid import pid_loop
from arduino import arduino_loop
from tracker import Tracker

if __name__ == "__main__":
    state = State()
    tracker = Tracker(state, track_shirt)
    tracker.connect_to_device(dev_idx=0)
    threading.Thread(target=pid_loop, args=[state]).start()
    threading.Thread(target=arduino_loop, args=[state, "/dev/tty.usbserial-DB00JLKU"]).start()
    tracker.loop()