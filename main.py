from timer import timer
timer('start')

import numpy as np
from alert import alert
from clear_terminal import clear_terminal
from vector_math import arbitrary_axis_rotation

clear_terminal()
class Camera():
    def __init__(self):
        pass
    def translate(self,change):
        assert change.shape == (3), f"change should be an array with three elements, not {change.shape}"
        self.position = self.position + change

    # assuming the vector is pointing towards you, 
    # counter clockwise is the positive direction of rotation
    def rotate_pitch(self,degrees):
        # y and z, x is the vector
        # nodding, upwards nod is positive
        
        cross = np.cross(camera.view_vector,camera.up_vector)
        print(f"cross:{cross}")
        self.up_vector   = arbitrary_axis_rotation(self.up_vector, cross, degrees)
        self.view_vector = arbitrary_axis_rotation(self.view_vector, cross, degrees)
        
    def rotate_yaw(self,degrees):
        # x and y, z is the vector
        # shaking head, left rotation is positive
        self.view_vector = arbitrary_axis_rotation(self.view_vector, self.up_vector, degrees)
    def rotate_roll(self,degrees):
        # x and z, y is the vector
        # side to side, indian head nod, rolling right is positive
        self.up_vector = arbitrary_axis_rotation(self.up_vector, self.view_vector, degrees)
camera = Camera()
camera.position    = np.array(( 0,-1, 0)) # x,y,z
camera.view_vector = np.array(( 0, 1, 0))
camera.up_vector   = np.array(( 0, 0, 1))
'''
print(f"view:{camera.view_vector}")
print(f"up:{camera.up_vector}")
camera.rotate_pitch(45)
print(f"view:{camera.view_vector}")
print(f"up:{camera.up_vector}")
'''
geometry = np.array([[-1,2,0],[1,2,0]])
# at this point in the pipeline all the geometry is defined relative to the world origin
# now, we make it relative to the camera, both the coordinates and the rotation

# step one is easy, subtract the camera position from every world coordinate

geometry = geometry-camera.position

# the second step is more difficult

# this is where the inverse of the view transformation is performed


