from video import CaptureFeed
from tracking import EyeTracker
from communications import Communicator


class DataManager:

    def __init__(self):
        self.camera = CaptureFeed()
        self.eye_tracker = EyeTracker()
        self.rpi_link = Communicator()
        self.data_filter = DataFilter()

    # def camera_test(self):
    #     while True:
    #         frame = self.camera.get_next_frame()
    #         self.eye_tracker.get_eye_info(frame)

    def get_and_process_frame(self):
        next_frame = self.camera.get_next_frame()
        eye_info = self.eye_tracker.get_eye_info(next_frame)
        self.data_filter.add_data_point(eye_info)
        self._handle_communications(eye_info)

    def _handle_communications(self, eye_info):
        right = eye_info.right_is_closed and self.data_filter.is_right_closed()
        left = eye_info.left_is_closed and self.data_filter.is_left_closed()
        if not (right and left):
            if right:
                self.rpi_link.send_up()
            elif left:
                self.rpi_link.send_down()
            else:
                x = self.data_filter.get_x()
                y = self.data_filter.get_y()
                self.rpi_link.send_delta(x, y)


class DataFilter:

    MAX_LEN = 1

    def __init__(self):
        self.filtered_x = 0
        self.filtered_y = 0
        self.filtered_right = [False for i in range(self.MAX_LEN)]
        self.filtered_left = [False for i in range(self.MAX_LEN)]
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

    def is_right_closed(self):
        return self._is_eye_closed(self.filtered_right)

    def is_left_closed(self):
        return self._is_eye_closed(self.filtered_left)

    def _is_eye_closed(self, filtered_eye):
        cnt = 0
        for i in range(len(filtered_eye)):
            if filtered_eye[i]:
                cnt += 1
        return cnt >= int(self.MAX_LEN / 2)

    def get_x(self):
        return self.filtered_x

    def get_y(self):
        return self.filtered_y
