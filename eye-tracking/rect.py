class Rect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def intersects(self, rect):
        a = rect.x > self.x + self.w
        b = rect.x + rect.w < self.x
        c = rect.y > self.y + self.h
        d = rect.y + rect.h < self.y

        return not (a or b or c or d)

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_w(self):
        return self.w

    def get_h(self):
        return self.h

    def get(self):
        return self.x, self.y, self.w, self.h
