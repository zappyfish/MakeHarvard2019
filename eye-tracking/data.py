from video import CaptureFeed
import cv2
from tracking import EyeTracker
from communications import Communicator

class DataManager:

    def __init__(self):
        self.camera = CaptureFeed()
        self.eye_tracker = EyeTracker()
        self.rpi_link = Communicator()
        self.data_filter = DataFilter()

    def camera_test(self):
        while True:
            frame = self.camera.get_next_frame()
            cv2.imshow('test', frame)
            cv2.waitKey(1)

    def get_and_process_frame(self):
        next_frame = self.camera.get_next_frame()
        eye_info = self.eye_tracker.get_eye_info(next_frame)
        self.data_filter.add_data_point(eye_info)

class DataFilter:

    MAX_LEN = 10

    def __init__(self):
        self.filtered_x = 0
        self.filtered_y = 0
        self.filtered_right = []
        self.filtered_left = []
        self.filter_ind = 0
        self.lpf_alpha = 0

    def add_data_point(self, eye_info):
        self.filtered_right[self.filter_ind] = eye_info.right_is_closed
        self.filtered_left[self.filter_ind] = eye_info.left_is_closed
        self.filter_ind += 1
        if self.filter_ind == self.MAX_LEN:
            self.filter_ind = 0
        self.filtered_x += self.lpf_alpha * (eye_info.x - self.filtered_x)
        self.filtered_y += self.lpf_alpha * (eye_info.y - self.filtered_y)

