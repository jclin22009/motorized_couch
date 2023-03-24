import numpy as np
from record3d import Record3DStream
import cv2
from threading import Event
from state import State

MIN_DETECTION_AREA = 2000

class Tracker:
    def __init__(self, state: State, tracker_fn, is_landscape=True):
        self.state = state
        self.event = Event()
        self.session = None
        self.DEVICE_TYPE__TRUEDEPTH = 0
        self.DEVICE_TYPE__LIDAR = 1
        self.tracker_fn = tracker_fn
        self.is_landscape = is_landscape

    def on_new_frame(self):
        """
        This method is called from non-main thread, therefore cannot be used for presenting UI.
        """
        self.event.set()  # Notify the main thread to stop waiting and process new frame.

    def on_stream_stopped(self):
        print('Stream stopped')

    def connect_to_device(self, dev_idx):
        print('Searching for devices')
        devs = Record3DStream.get_connected_devices()
        print('{} device(s) found'.format(len(devs)))
        for dev in devs:
            print('\tID: {}\n\tUDID: {}\n'.format(dev.product_id, dev.udid))

        if len(devs) <= dev_idx:
            raise RuntimeError('Cannot connect to device #{}, try different index.'
                               .format(dev_idx))

        dev = devs[dev_idx]
        self.session = Record3DStream()
        self.session.on_new_frame = self.on_new_frame
        self.session.on_stream_stopped = self.on_stream_stopped
        self.session.connect(dev)  # Initiate connection and start capturing

    def get_intrinsic_mat_from_coeffs(self, coeffs):
        return np.array([[coeffs.fx,         0, coeffs.tx],
                         [        0, coeffs.fy, coeffs.ty],
                         [        0,         0,         1]])

    def loop(self):
        while True:
            self.event.wait()

            # Retrieve depth and color maps
            depth = self.session.get_depth_frame()
            rgb = self.session.get_rgb_frame()
            intrinsic_mat = self.get_intrinsic_mat_from_coeffs(self.session.get_intrinsic_mat())
            if self.session.get_device_type() == self.DEVICE_TYPE__TRUEDEPTH:
                depth = cv2.flip(depth, 1)
                rgb = cv2.flip(rgb, 1)
            rgb = cv2.cvtColor(rgb, cv2.COLOR_RGB2BGR)

            # Find shirt
            rgb_with_shirt, cx, cy, w, h = self.tracker_fn(rgb)

            sol = np.linalg.inv(intrinsic_mat) @ np.array([cx, cy, 1])
            z = depth[cy * depth.shape[0] // rgb.shape[0], cx * depth.shape[1] // rgb.shape[1]]
            x = (sol[0] * z) / sol[2]
            y = -(sol[1] * z) / sol[2]

            if w * h < MIN_DETECTION_AREA:
                self.state.stopped = True
            else:
                self.state.stopped = False

            if self.is_landscape:
                self.state.x = y
                self.state.y = -x
            else:
                self.state.x = x
                self.state.y = y
            self.state.z = z

            # Show the color and depth images
            cv2.imshow('RGB', rgb_with_shirt)
            cv2.imshow('Depth', depth)
            cv2.waitKey(1)

            self.event.clear()