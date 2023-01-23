from clear_terminal import clear_terminal
clear_terminal()

from alert import alert

import ray_cast
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
camera.origin      = np.array(( 0,-10, 0)) # x,y,z
camera.view_vector = np.array(( 0,  1, 0))
camera.up_vector   = np.array(( 0,  0, 1))

alert('<initializing pygame>')
import pygame
pygame.init()
h_res, v_res = 500,500#1920/1.25,1000/1.25
screen = pygame.display.set_mode((h_res, v_res))

clock = pygame.time.Clock()

from geometry_pipeline import project_in_camera_space
from geometry_pipeline import project_in_screen_space
from geometry_pipeline import project_screen_coordinates

import time


from attempt import a
from object import Object, OBJ
#cat = Object(geometry=a, name='cat')
print('<importing model>')
#teapot = OBJ('models/teapot')
triangle = OBJ('models/triangle')
triangle.name = 'triangle'

cube = OBJ('models/cube')
cube.name = cube
print('<importing Mesh>')
from mesh import Mesh
print('<importing render>')
from render import render
print('<importing Scene>')
from scene import Scene
#teapot.rotate(90, axis='X',local=False)




# priaga

scene = Scene(camera=camera)
scene.add_object( cube )



#cat.origin_to_geometry()
#teapot.origin_to_geometry()
x = 0.
count = 0.
alert('<running loop>')
while True:
    tic = time.time()
    # Process player inputs.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
    alert('<rotating>')
    #.rotate(1, axis='Z',local=False)
    
    #teapot.rotate(4.5, axis='Z',local=False)
    #teapot.rotate(1, axis='X',local=True)
    #timer('rotating')
    cube.rotate(1, axis='z',local=True)
    #timer('rotating')
    alert('<rendering>')
    image = render(screen=screen, scene=scene)
    alert('<blitting>')
    screen.blit(image, (0,0) )
    #camera.translate(np.array([0,-0.1,0]))
    pygame.display.flip()  # Refresh on-screen display
    clock.tick(10)         # wait until next frame (at 60 FPS)
    toc = time.time()
    clear_terminal()
    frames = round(1/(toc-tic),2)
    x += frames
    count += 1
    print(f'fps:\t{frames}')
    print(f'avg fps:\t{round(x/count,2)}')
    
    timer('')
    #quit()



print("<end of program>")