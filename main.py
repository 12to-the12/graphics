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
camera.position    = np.array(( 0, -50, 0)) # x,y,z
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


'''
from ray_cast import ray_cast
from ray_cast import generate_rays
geometry = generate_rays(10,10,2, random=True, norm=True)
geometry = np.concatenate([np.array([[0,0,0]]),generate_rays(10,10,2, random=True, norm=False),geometry])
ray_cast(screen=screen,camera=camera)
'''
import time
alert('<running loop>')

from attempt import a
from object import Object
cat = Object(geometry=a, name='cat')

from mesh import Mesh
from render import render
from scene import Scene
# triaga
mesh = Mesh()
mesh.build(Object.get_objects() )
cat.origin_to_geometry()
while True:
    tic = time.time()
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    # Do logical updates here.
    # ...
    cat.rotate(1, axis='Z',local=False)
    cat.rotate(1, axis='Z',local=True)
    #cat.scale(1.01)
    #camera.translate(np.array([0,0.1,0]))
    timer('rotate geometry')
    mesh.build(Object.get_objects() )
    timer('build')
    geo = project_in_camera_space(mesh.geometry, camera)
    coords   = project_in_screen_space(geo, camera)
    coords   = project_screen_coordinates(coords, screen)
    timer('project')
    screen.fill("white")  # Fill the display with a solid color
    for coord in coords:
        pygame.draw.circle(screen, (0,0,0), coord, 1)
    # Render the graphics here.
    # ...
    timer('draw')
    pygame.display.flip()  # Refresh on-screen display
    timer('flip')
    #clock.tick(60)         # wait until next frame (at 60 FPS)
    toc = time.time()
    clear_terminal()
    print(coords.shape)
    print(round(1/(toc-tic)))

print("<end of program>")