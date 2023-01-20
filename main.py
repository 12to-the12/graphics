from clear_terminal import clear_terminal
clear_terminal()

from alert import alert
alert('<importing>')


from timer import timer
from vector_math import arbitrary_axis_rotation, normalize
from vector_math import orthogonal, angle
import random


alert('<initializing numpy>')
# initialize numpy
import numpy as np
np.set_printoptions(suppress=True) # suppresses scientific notation




alert('<initializing camera>')
from camera import Camera
camera = Camera()
camera.position    = np.array(( 0, -100, 0)) # x,y,z
camera.view_vector = np.array(( 0, 1, 0))
camera.up_vector   = np.array(( 0, 0, 1))



alert('<rotating camera>')
camera.rotate_yaw(0) # left
camera.rotate_pitch(0) # up
camera.rotate_roll(0) #



alert('<initializing pygame>')
import pygame
pygame.init()
h_res, v_res = 1000,500#1920/1.25,1000/1.25
screen = pygame.display.set_mode((h_res, v_res))

clock = pygame.time.Clock()

alert('<initializing geometry>')
geometry = np.array([
    [-2,2,-2],[-2,2,2],[2,2,-2],[2,2,2],
    [-2,2,-2],[-2,2,2],[2,2,-2],[2,2,2],
    [-2,-2,-2],[-2,-2,2],[2,-2,-2],[2,-2,2],
    [-2,-2,-2],[-2,-2,2],[2,-2,-2],[2,-2,2]
    ])
from geometry_pipeline import project_in_camera_space
from geometry_pipeline import project_in_screen_space
from geometry_pipeline import project_screen_coordinates

alert('<projecting geometry>')



print()

from attempt import a
geometry = a
#geometry *= [2,1,1]
alert('<running loop>')
while True:
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    # Do logical updates here.
    # ...
    camera.translate(np.array([0, 0.1,0.1]))
    geometry = arbitrary_axis_rotation(geometry, np.array([0,0,1]), 1)
    geo = project_in_camera_space(geometry, camera)
    coords   = project_in_screen_space(geo, camera)
    coords   = project_screen_coordinates(coords, screen)

    screen.fill("white")  # Fill the display with a solid color
    for coord in coords:
        #print(coord)
        pygame.draw.circle(screen, (0,0,0), coord, 1)
    # Render the graphics here.
    # ...
    pygame.display.flip()  # Refresh on-screen display
    clock.tick(10)         # wait until next frame (at 60 FPS)