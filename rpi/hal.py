from motors import Motor, ReverseMotor
#from testing import TestMotor
from math import sin, cos, pi
import numpy as np

class HardwareAbstractionLayer:

    ARM_ONE_LENGTH = 1
    ARM_TWO_LENGTH = 1
    Z_MOVEMENT_FACTOR = 5
    ANGLE_DISPLACEMENT_MAGNITUDE = 0.05

    def __init__(self):
        z_pin = 18
        angle_one_pin = 13
        angle_two_pin = 12

        self.z_motor = Motor(z_pin)
        self.shoulder_motor = Motor(angle_one_pin, 80 * pi / 180)
        self.elbow_motor = Motor(angle_two_pin, 105 * pi / 180)

    def translate_instrument(self, delta_x, delta_y):
        desired = np.array([delta_x, delta_y])
        theta_one = self.shoulder_motor.get_angle()
        theta_two = self.elbow_motor.get_angle()
        jacobian = self.compute_jacobian(theta_one, theta_two)

        control_inputs = np.linalg.lstsq(jacobian, desired)[0]
        if control_inputs[0] != 0 and control_inputs[1] != 0:
            # control_inputs[1] = -control_inputs[1]
            control_inputs[0] = -control_inputs[0] # TODO: check this
            control_inputs = self.remap_controls(control_inputs)
            return self.shoulder_motor.change_angle(control_inputs[0]) and self.elbow_motor.change_angle(control_inputs[1])
        else:
            return False

    def remap_controls(self, control_inputs):
        return control_inputs * (self.ANGLE_DISPLACEMENT_MAGNITUDE / np.linalg.norm(control_inputs))

    def move_instrument_up(self):
        return self.z_motor.change_angle(self.Z_MOVEMENT_FACTOR)

    def move_instrument_down(self):
        return self.z_motor.change_angle(-self.Z_MOVEMENT_FACTOR)

    def compute_jacobian(self, theta_one, theta_two):
        l1 = self.ARM_ONE_LENGTH
        l2 = self.ARM_TWO_LENGTH
        t1 = theta_one
        t2 = theta_two
        dx_dt1 = l1 * sin(t1) - l2 * sin(t1 + t2)
        dx_dt2 = -l2 * sin(t1 + t2)

        dy_dt1 = l1 * cos(t1) + l2 * cos(t1 + t2)
        dy_dt2 = l2 * cos(t1 + t2)

        return np.array([[dx_dt1, dx_dt2], [dy_dt1, dy_dt2]])

    def test_move(self, x, y, r=20):
        for i in range(r):
            self.translate_instrument(x, y)