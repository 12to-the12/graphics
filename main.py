from clear_terminal import clear_terminal
clear_terminal()

from alert import alert
alert('<importing>')

from timer import timer
from vector_math import arbitrary_axis_rotation, normalize
from vector_math import orthogonal, angle
import random

alert('<initializing numpy>')
import numpy as np
np.set_printoptions(suppress=True) # suppresses scientific notation

alert('<initializing camera>')
from camera import Camera
camera = Camera()
camera.position    = np.array(( 0, -50, 0)) # x,y,z
camera.view_vector = np.array(( 0, 1, 0))
camera.up_vector   = np.array(( 0, 0, 1))

alert('<initializing pygame>')
import pygame
pygame.init()
h_res, v_res = 1000,500#1920/1.25,1000/1.25
screen = pygame.display.set_mode((h_res, v_res))

clock = pygame.time.Clock()

cube = np.array([
    [-2., 2.,-2.],[-2., 2., 2.],[ 2., 2.,-2.],[ 2., 2., 2.],
    [-2., 2.,-2.],[-2., 2., 2.],[ 2., 2.,-2.],[ 2., 2., 2.],
    [-2.,-2.,-2.],[-2.,-2., 2.],[ 2.,-2.,-2.],[ 2.,-2., 2.],
    [-2.,-2.,-2.],[-2.,-2., 2.],[ 2.,-2.,-2.],[ 2.,-2., 2.]
    ])
from geometry_pipeline import project_in_camera_space
from geometry_pipeline import project_in_screen_space
from geometry_pipeline import project_screen_coordinates


import time
alert('<running loop>')

from attempt import a
from object import Object
cat = Object(geometry=a, name='cat')

from mesh import Mesh
from render import render
from scene import Scene
# triaga

scene = Scene()
scene.add_object( cat )
scene.camera = camera

cat.origin_to_geometry()
x = 0
count = 0
while True:
    tic = time.time()
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
    timer('event loop')
            
    cat.rotate(1, axis='Z',local=False)
    timer('rotating')
    cat.rotate(1, axis='Z',local=True)
    timer('rotating')
    image = render(canvas=screen, scene=scene)
    
    screen.blit(image, (0,0) )
    timer('blitting')
    pygame.display.flip()  # Refresh on-screen display
    #clock.tick(60)         # wait until next frame (at 60 FPS)
    toc = time.time()
    clear_terminal()
    frames = round(1/(toc-tic))
    x += frames
    count += 1
    print( round(x/count,2) )
    print( frames)
    timer('')



print("<end of program>")