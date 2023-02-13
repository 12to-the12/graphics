#!/usr/bin/env python3.10.9

from clear_terminal import clear_terminal
clear_terminal()

from alert import alert

import ray_cast
alert('<importing>')

from timer import timer, pprint, dump
from vector_math import arbitrary_axis_rotation, normalize
from vector_math import orthogonal, angle
import random

alert('<initializing numpy>')
import numpy as np
np.set_printoptions(suppress=True) # suppresses scientific notation

alert('<initializing pygame>')
import pygame
pygame.init()
h_res, v_res = 1920/1.25,1000/1.25
screen = pygame.display.set_mode((h_res, v_res))

alert('<initializing camera>')
from camera import Camera

camera = Camera( aspect_ratio = (h_res/v_res)   )
camera.origin      = np.array(( 0, -15, 0)) # x,y,z
camera.view_vector = np.array(( 0,  1, 0))
camera.up_vector   = np.array(( 0,  0, 1))



clock = pygame.time.Clock()

from geometry_pipeline import project_in_camera_space
from geometry_pipeline import project_in_screen_space
from geometry_pipeline import project_screen_coordinates

import time


from attempt import a
from object import Object, OBJ
#cat = Object(geometry=a, name='cat')
#cat.translate(np.array([0,20,0]))
#cat.origin_to_geometry()
print('<importing model>')
#teapot = OBJ('models/teapot')
triangle = OBJ('models/triangle')
triangle.name = 'triangle'

cube = OBJ('models/cube')
cube.name = 'cube'

teapot = OBJ('models/teapot')
teapot.name = 'teapot'

teapotb = OBJ('models/teapot')
teapotb.name = 'teapot'

teapotc = OBJ('models/teapot')
teapotc.name = 'teapot'
print('<importing Mesh>')
from mesh import Mesh
print('<importing render>')
from render import render
print('<importing Scene>')
from scene import Scene
#teapot.rotate(90, axis='X',local=False)





scene = Scene(camera=camera)
scene.add_object( teapot )
#scene.add_object( teapotb )
#scene.add_object( teapotc )


#teapotb.translate(np.array([10,0,0]))
#teapotc.translate(np.array([-10,0,0]))


cube.origin_to_geometry()
teapot.origin_to_geometry()

teapot.rotate(90, axis='x',local=False)


total_time   = 0.
total_frames = 0.
alert('<running loop>')
t = 1/60
while True:
    timer('top')
    tic = time.time()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
    #.rotate(1, axis='Z',local=False)
    
    

    mag = t # one degree per second
    teapot.rotate(mag*10, axis='z',local=False)
    #teapot.rotate(mag*2, axis='x',local=True)
    cube.rotate(mag*20, axis='z',local=False)
    cube.rotate(mag*20, axis='x',local=True)
    
    #teapotb.rotate(mag*2, axis='y',local=False)
    #teapotb.rotate(mag*3, axis='z',local=True)

    #teapotc.rotate(mag*3, axis='x',local=False)
    #teapotc.rotate(mag*2, axis='y',local=True)

    #triangle.rotate(1, axis='z',local=False)
    #cube.rotate( mag, axis='z',local=False)
    #cube.rotate(mag*2, axis='x',local=True)
    timer('rotation')

    tikk = time.time()
    image = render(screen=screen, scene=scene)
    tokk = time.time()
    pprint('render',tokk-tikk)
    screen.blit(image, (0,0) )
    #camera.translate(np.array([0,-0.1,0]))
    pygame.display.flip()  # Refresh on-screen display

    timer('flip')
    toc = time.time()
    t = (toc-tic)
    
    
    
    fps = round(1/t,2)
    pprint('',0)
    pprint('fps',fps)
    
    total_time += t
    total_frames += 1
    pprint('avg fps',total_frames/total_time)
    

    
    
    #clock.tick(60)
    timer('clock tick')
    dump()
    timer('printout')




print("<end of program>")