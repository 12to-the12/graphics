from timer import timer
timer('start')

import numpy as np
from alert import alert
from clear_terminal import clear_terminal
from vector_math import arbitrary_axis_rotation, normalize
from vector_math import orthogonal, angle
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

