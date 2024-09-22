import numpy as np
from scripts.vector_math import (
    single__axis_rotation,
    arbitrary_axis_rotation,
    normalize,
)
from scripts.vector_math import orthogonal, angle
from utilities.clear_terminal import clear_terminal
from math import atan
from scripts.entity import Entity
import numpy as np
from utilities.vectors import *
from utilities.config import config

cam_config = config.camera


class Camera(Entity):
    """a camera entity derived from the entity class"""

    def __init__(
        self,
        origin=world_origin,
        aspect_ratio=None,
        sensor_height=None,  # mm
        focal_length=cam_config.focal_length,
        sensor_width=cam_config.sensor_width,  # mm
        close_cull=cam_config.close_cull,
        far_cull=cam_config.far_cull,
    ):
        """aspect ratio is width over height, ergo width if height was one"""
        super().__init__(origin=origin, view_vector=n_Z, up_vector=Y)
        self.focal_length = focal_length
        self.sensor_width = sensor_width
        self.close_cull = close_cull
        self.far_cull = far_cull

        if aspect_ratio is None:
            self.sensor_height = sensor_height
            self.aspect_ratio = self.sensor_width / self.sensor_height
        elif sensor_height is None:
            self.aspect_ratio = aspect_ratio
        else:
            raise Exception("either the aspect ratio or height needs to be defined")
        self.fov = 2 * atan(sensor_width / (2 * focal_length))  # had to be radians

        self.focal_ratio = focal_length / sensor_width  # f-number

    @property
    def horizontal_field_of_view(self) -> float:
        return atan(self.sensor_width / (2 * self.focal_length)) * 2  # radians

    @property
    def vertical_field_of_view(self) -> float:
        return atan(self.sensor_height / (2 * self.focal_length)) * 2  # radians

    def orient(self):
        """this function returns the pair of axes and angles
        necessary to rotate the camera's position towards -Z, +Y
        these can be used to apply the inverse to vertexes in the scene
        to make them rotate relative to the camera
        
        """
        Z = np.array([0.0, 0.0, 1.0])  #  Z
        n_Z = np.array([0.0, 0.0, -1.0])  # -Z
        Y = np.array([0.0, 1.0, 0.0])  # +Y
        X = np.array([1.0, 0.0, 0.0])  # +X

        angle_a = angle(self.view_vector, n_Z)

        if angle_a == 180:
            intermediary_up = single__axis_rotation(self.up_vector, X, 180)
            axis_a = None
        elif angle_a:  # only necessary if angle_a is non zero
            axis_a = orthogonal(self.view_vector, n_Z)  # computed axis of rotation
            # intermediary is the result of applying the operation that aligns the
            # view vector with -Z to the up vector
            intermediary_up = single__axis_rotation(self.up_vector, axis_a, angle_a)
        else:
            intermediary_up = self.up_vector
            axis_a = n_Z

        # the next step is to align the up vector with +Y

        angle_b = angle(intermediary_up, Y)

        if angle_b == 180:
            axis_b = n_Z
        elif angle_b:  # only necessary if angle_a is non zero
            axis_b = orthogonal(intermediary_up, Y)  # computed axis of rotation
            # intermediary is the result of applying the operation that aligns the
            # view vector with -Z to the up vector
        else:
            axis_b = n_Z

        return [axis_a, angle_a, axis_b, angle_b]


if __name__ == "__main__":
    np.set_printoptions(suppress=True)  # suppresses scientific notation
    clear_terminal()
    camera = Camera()
    camera.origin = np.array((0, -1, 0))  # x,y,z
    camera.view_vector = np.array((0, 1, 0))
    camera.up_vector = np.array((0, 0, 1))

    for x in [-180, 0, 180, 360, 50]:
        camera.rotate_yaw(x)  # left
        camera.rotate_pitch(x)  # up
        camera.rotate_roll(x)  # up

        camera.orient()
