import RPi.GPIO as GPIO
from math import pi


class Motor:

    START_ANGLE = 45
    MAX_ANGLE = 90
    MIN_ANGLE = 0

    def __init__(self, motor_pin):
        GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme
        pwm_pin = GPIO.setup(motor_pin, GPIO.OUT)
        self.angle = self.START_ANGLE
        self.pwm = GPIO.PWM(pwm_pin, 1000)  # 90 is start angle
        self.pwm.start(50) # change this
        print("started")

    def set_angle(self, angle):
        if self.can_set_angle(angle):
            self.pwm.changeDutyCycle(self._map_angle_to_dc(angle))
            self.angle = angle
            print("changed angle to: " + str(self.angle))
            return True
        else:
            print("could not change to angle" + str(self.angle))
            return False

    def _map_angle_to_dc(self, angle):
        return int(self.MAX_ANGLE * (angle / pi))

    def get_angle(self):
        return self.angle

    def can_set_angle(self, angle):
        return self.MIN_ANGLE <= angle <= self.MAX_ANGLE
