import cv2

# hs 485 hb servo
class CaptureFeed:

    def __init__(self):
        self.input = cv2.VideoCapture(0)

    def get_next_frame(self):
        ret, frame = self.input.read()
        return frame
