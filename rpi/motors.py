import wiringpi
from math import pi


class Motor:

    MAX_DC = 256
    START_SIGNAL = int(MAX_DC / 2)
    MIN_DC = 0
    PWM_ANGLE_SCALE_FACTOR = (pi / 128)

    def __init__(self, motor_pin):
        wiringpi.wiringPiSetupGpio()
        self.pwm = motor_pin
        wiringpi.pinMode(self.pwm, wiringpi.GPIO.PWM_OUTPUT)
        wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
        self.pwm_signal = self.START_SIGNAL
        wiringpi.pwmSetClock(192)  # TODO: check this
        wiringpi.pwmSetRange(2000)
        wiringpi.pwmWrite(self.pwm, self.pwm_signal)

    def change_angle(self, angle):
        pwm = self._map_angle_to_dc(angle) + self.pwm_signal
        if self.can_set_pwm_to(pwm):
            wiringpi.pwmWrite(self.pwm, int(pwm))
            self.pwm_signal = pwm
            print("signal set to ")
            print(pwm)
            return True
        else:
            print("could not set to: ")
            print(pwm)
            return False

    def _map_angle_to_dc(self, angle):
        return angle

    def get_angle(self):
        return self.pwm_signal * self.PWM_ANGLE_SCALE_FACTOR

    def can_set_pwm_to(self, pwm):
        return self.MIN_DC <= pwm <= self.MAX_DC
