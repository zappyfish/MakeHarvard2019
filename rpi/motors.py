import wiringpi
from math import pi


class Motor:

    START_ANGLE = 45
    MAX_ANGLE = 90
    MIN_ANGLE = 0

    def __init__(self, motor_pin):
        wiringpi.wiringPiSetupGpio()
        self.pwm = motor_pin
        wiringpi.pinMode(self.pwm, wiringpi.GPIO_PWM_OUTPUT)
        wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
        self.angle = self.START_ANGLE
        wiringpi.pwmSetClock(192) # TODO: check this
        wiringpi.pwmSetRange(2000)
        wiringpi.pwmWrite(self.pwm, self.angle)
        print("started")

    def set_angle(self, angle):
        if self.can_set_angle(angle):
            self.pwm.ChangeDutyCycle(self._map_angle_to_dc(angle))
            self.angle = angle
            print("changed angle to: " + str(self.angle))
            return True
        else:
            print("could not change to angle" + str(self.angle))
            return False

    def _map_angle_to_dc(self, angle):
        return angle

    def get_angle(self):
        return self.angle

    def can_set_angle(self, angle):
        return self.MIN_ANGLE <= angle <= self.MAX_ANGLE
