import wiringpi
from math import pi


class Motor:

    MAX_DC = 256
    START_SIGNAL = int(MAX_DC / 2)
    MIN_DC = 0
    PWM_ANGLE_SCALE_FACTOR = (pi / 128)

    DC_SCALE_FACTOR = 4

    def __init__(self, motor_pin, start_angle_offset=0):
        wiringpi.wiringPiSetupGpio()
        self.pwm = motor_pin
        wiringpi.pinMode(self.pwm, wiringpi.GPIO.PWM_OUTPUT)
        wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
        self.pwm_signal = self.START_SIGNAL
        self.start_angle_offset = start_angle_offset
        wiringpi.pwmSetClock(192)  # TODO: check this
        wiringpi.pwmSetRange(2000)
        wiringpi.pwmWrite(self.pwm, self.pwm_signal)

    def change_angle(self, angle):
        start_angle = self.get_angle()
        angle = -angle
        pwm = self._map_angle_to_dc(angle) + self.pwm_signal
        if self.can_set_pwm_to(pwm):
            wiringpi.pwmWrite(self.pwm, int(pwm))
            self.pwm_signal = pwm
            print("angle change: ")
            print(self.get_angle() - start_angle)
            return True
        else:
            print("could not change")
            return False

    def _map_angle_to_dc(self, angle):
        return angle * self.DC_SCALE_FACTOR

    def get_angle(self):
        return ((self.pwm_signal - self.START_SIGNAL) * self.PWM_ANGLE_SCALE_FACTOR) + self.start_angle_offset

    def can_set_pwm_to(self, pwm):
        return self.MIN_DC <= pwm <= self.MAX_DC
