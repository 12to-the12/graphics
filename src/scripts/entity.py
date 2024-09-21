import numpy as np
from scripts.vector_math import single__axis_rotation, orthogonal, angle
from utilities.timer import t
from utilities.tree import tree
from utilities.analysis import analyze
from utilities.vectors import *

import time


class Entity:
    def __init__(self, origin=world_origin, view_vector=Y, up_vector=Z):
        self.origin = world_origin
        self.view_vector = view_vector
        self.up_vector = up_vector

        self.scale_factor = 1

        # these don't work, something to think about later
        # self.z_rotation = angle(ignore(self.view_vector,'z'),  Y)
        # self.y_rotation = angle(ignore(self.view_vector,'y'),  Y)
        # self.x_rotation = angle(ignore(self.view_vector,'x'),n_Z)

    def __str__(self) -> str:
        return f"view_vector: {self.view_vector}"

    def translate(self, change):
        if type(change) is list:
            change = np.array(change)
        assert change.shape == (
            3,
        ), f"change should be an array with three elements, not {change.shape}"
        self.origin = self.origin + change

    def scale(self, factor):
        """scales in every direction equally"""
        self.scale_factor *= factor

    def rot_axis(self, axis, degrees):
        """rotates the entity around the given axis"""
        self.view_vector = single__axis_rotation(self.view_vector, axis, degrees)
        self.up_vector = single__axis_rotation(self.up_vector, axis, degrees)

    # @analyze
    def rotate(self, degrees, local=False, axis="z"):
        """the user accessed rotate command
        for the local rotations the view_vector acts as the Y axis, the up_vector acts as
        the Z, and the orthogonal between them acts as the X"""
        axis_letter = axis

        if local:
            if axis_letter == "x":
                axis = np.cross(self.view_vector, self.up_vector)
            elif axis_letter == "y":
                axis = self.view_vector
            elif axis_letter == "z":
                axis = self.up_vector
            else:
                raise Exception("axis_letter must be xyz")
        else:

            if axis_letter == "x":
                axis = X
            elif axis_letter == "y":
                axis = Y
            elif axis_letter == "z":
                axis = Z
            else:
                raise Exception(f"axis_letter must be xyz, not {axis_letter}")

        self.rot_axis(axis, degrees)

        return axis

    # these rotations operate in camera space
    # assuming the vector is pointing towards you,
    # counter clockwise is the positive direction of rotation
    def rotate_pitch(self, degrees):
        """y and z, x is the vector nodding, upwards nod is positive"""
        cross = np.cross(self.view_vector, self.up_vector)
        self.up_vector = single__axis_rotation(self.up_vector, cross, degrees)
        self.view_vector = single__axis_rotation(self.view_vector, cross, degrees)

    def rotate_yaw(self, degrees):
        """x and y, z is the vector shaking head, left rotation is positive"""
        self.view_vector = single__axis_rotation(
            self.view_vector, self.up_vector, degrees
        )

    def rotate_roll(self, degrees):
        """x and z, y is the vector side to side, indian head nod, rolling right is positive"""
        self.up_vector = single__axis_rotation(
            self.up_vector, self.view_vector, degrees
        )
