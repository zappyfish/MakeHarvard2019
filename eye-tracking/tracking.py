
class EyeTracker:

    def __init__(self):
        pass

    def get_eye_info(self, frame):
        return EyePacket(False, False, 0, 0)


class EyePacket:

    def __init__(self, right_is_closed, left_is_closed, x, y):
        self.right_is_closed = right_is_closed
        self.left_is_closed = left_is_closed
        self.x = x
        self.y = y
