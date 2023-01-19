from timer import timer
timer('start')

import numpy as np
from alert import alert
from clear_terminal import clear_terminal
from vector_math import arbitrary_axis_rotation
from vector_math import normalize
import random
from camera import Camera

np.set_printoptions(suppress=True) # suppresses scientific notation

clear_terminal()

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


camera.rotate_yaw(45) # left
camera.rotate_pitch(45) # up
#camera.rotate_roll(45) # right

geometry = np.array([[-1,2,0],[1,2,0]])
# at this point in the pipeline all the geometry is defined relative to the world origin
# now, we make it relative to the camera, both the coordinates and the rotation

# step one is easy, subtract the camera position from every world coordinate

geometry = geometry-camera.position

# the second step is more difficult

# this is where the inverse of the view transformation is performed
# the world will be oriented with the camera pointeed straight down,
# with the view vector towards -Z and the up vector towards +Y






#this system works but used arbitrary axes


axis_a = np.cross(camera.view_vector,n_Z) # computed axis of rotation

angle_a = np.arccos(np.dot(camera.view_vector,n_Z))
angle_a = np.degrees(angle_a)


# intermediary is the result of applying the operation that aligns the
# view vector with -Z to the up vector
intermediary = arbitrary_axis_rotation(camera.up_vector,axis_a,angle_a)
# the next step is to align the up vector with +Y


axis_b = np.cross(intermediary,Y) # computed axis of rotation

angle_b = np.arccos(np.dot(intermediary,Y))
angle_b = np.degrees(angle_b)


print(f"angle a:\t{angle_a}")
print(f"angle b:\t{angle_b}")
