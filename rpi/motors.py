import wiringpi
from math import pi


class Motor:

    START_ANGLE = 512
    MAX_DC = 1024
    MIN_DC = 0
    PWM_ANGLE_SCALE_FACTOR = 1.0

    def __init__(self, motor_pin):
        wiringpi.wiringPiSetupGpio()
        self.pwm = motor_pin
        wiringpi.pinMode(self.pwm, wiringpi.GPIO.PWM_OUTPUT)
        wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
        self.pwm_signal = 0
        wiringpi.pwmSetClock(192) # TODO: check this
        wiringpi.pwmSetRange(2000)
        wiringpi.pwmWrite(self.pwm, self.pwm_signal)
        print("started")

    def change_angle(self, angle):
        pwm = self._map_angle_to_dc(angle) + self.pwm
        if self.can_set_angle(angle):
            wiringpi.pwmWrite(self.pwm, self._map_angle_to_dc(angle))
            self.pwm_signal = pwm
        return self.get_angle()

    def _map_angle_to_dc(self, angle):
        return int(angle * 20)

    def get_angle(self):
        return self.pwm_signal * self.PWM_ANGLE_SCALE_FACTOR

    def can_set_angle(self, angle):
        return self.MIN_DC <= self._map_angle_to_dc(angle) <= self.MAX_DC
