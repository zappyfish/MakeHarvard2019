from motors import Motor
#from testing import TestMotor
from math import sin, cos
import numpy as np

class HardwareAbstractionLayer:

    ARM_ONE_LENGTH = 1
    ARM_TWO_LENGTH = 1
    Z_MOVEMENT_FACTOR = 5

    def __init__(self):
        z_pin = 13
        angle_one_pin = 12
        angle_two_pin = 18

        self.z_motor = Motor(z_pin)
        self.shoulder_motor = Motor(angle_one_pin)
        self.elbow_motor = Motor(angle_two_pin)


    def translate_instrument(self, delta_x, delta_y):
        desired = np.array([delta_x, delta_y])
        theta_one = self.shoulder_motor.get_angle()
        theta_two = self.elbow_motor.get_angle()
        jacobian = self.compute_jacobian(theta_one, theta_two)

        control_inputs = np.linalg.lstsq(jacobian, desired)[0]
        success = self.shoulder_motor.change_angle(control_inputs[0]) and self.elbow_motor.change_angle(control_inputs[1])
        return success

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