from math import cos, sin

class TestMotor:

    def __init__(self, pin_number):
        self.angle = 0

    def get_angle(self):
        return self.angle

    def set_angle(self, angle):
        self.angle = angle

def compute_position(motor1, motor2):
    # Assume length of 1 for both
    t1 = motor1.angle
    t2 = motor2.angle
    p1 = [cos(t1) + cos(t1 + t2), sin(t1) + sin(t1 + t2)]
    return p1

if __name__ == '__main__':
    from hal import HardwareAbstractionLayer

    myhal = HardwareAbstractionLayer()

    m1 = myhal.shoulder_motor
    m2 = myhal.elbow_motor

    for i in range(100):
        myhal.translate_instrument(-0.01, 0.01)

    print(compute_position(m1, m2))

