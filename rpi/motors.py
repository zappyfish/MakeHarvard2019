import wiringpi
from math import pi


class Motor(object):

    MAX_DC = 256
    START_SIGNAL = int(MAX_DC / 2)
    MIN_DC = 0
    PWM_ANGLE_SCALE_FACTOR = 128 / pi

    DC_SCALE_FACTOR = 4

    def __init__(self, motor_pin, start_angle_offset=0):
        wiringpi.wiringPiSetupGpio()
        self.pwm = motor_pin
        wiringpi.pinMode(self.pwm, wiringpi.GPIO.PWM_OUTPUT)
        wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
        self.angle = start_angle_offset
        wiringpi.pwmSetClock(192)  # TODO: check this
        wiringpi.pwmSetRange(2000)
        wiringpi.pwmWrite(self.pwm, int(self._map_angle_to_dc(self.angle)))

    def change_angle(self, angle):
        start_angle = self.get_angle()
        print("start angle: ")
        print(start_angle)
        pwm = self._map_angle_to_dc(angle + self.get_angle())
        if self.can_set_pwm_to(pwm):
            wiringpi.pwmWrite(self.pwm, int(pwm))
            self.angle += angle
            print("end angle: ")
            print(self.get_angle())
            return True
        else:
            print("could not change")
            return False

    def _map_angle_to_dc(self, angle):
        return (angle * self.PWM_ANGLE_SCALE_FACTOR) + self.START_SIGNAL

    def get_angle(self):
        return self.angle

    def can_set_pwm_to(self, pwm):
        return self.MIN_DC <= pwm <= self.MAX_DC

class ReverseMotor(Motor):

    def __init__(self, motor_pin, start_angle_offset=0):
        super(ReverseMotor, self).__init__(motor_pin, start_angle_offset)
        self.applied_angle = self.angle
        self.angle *= -1

    def change_angle(self, angle):
        start_angle = self.get_angle()
        print("start angle: ")
        print(start_angle)
        pwm = self._map_angle_to_dc(self.applied_angle - self.angle)
        if self.can_set_pwm_to(pwm):
            wiringpi.pwmWrite(self.pwm, int(pwm))
            self.angle += angle
            self.applied_angle -= angle
            print("end angle: ")
            print(self.get_angle())
            return True
        else:
            print("could not change")
            return False