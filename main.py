#!/usr/bin/env python3.10.9
from clear_terminal import clear_terminal
clear_terminal()
from alert import alert
alert('<fetching>')
import fetch
clear_terminal()
alert('<fetched>')

from config import config
from timer import t, fps
import timer
from analysis import analyze, dump
import time
import random

import numpy as np
np.set_printoptions(suppress=True) # suppresses scientific notation

alert('<initializing pygame>')
import pygame
pygame.init()
h_res = config['window']['h_res']
v_res = config['window']['v_res']
screen = pygame.display.set_mode((h_res, v_res))
clock = pygame.time.Clock()

alert('<initializing camera>')
from camera import Camera
camera = Camera( aspect_ratio = (h_res/v_res),**config['camera'] )

camera.rotate(90,axis='x')



camera.translate([0,-15,0])

from models.attempt import a
from object import Scene_Object, OBJ


# triangle = OBJ('models/triangle')
# triangle.name = 'triangle'

# cube = OBJ('models/cube')
# cube.name = 'cube'

# # cat = OBJ('models/cat')
# # cat.name = 'cat'

teapot = OBJ('models/teapot')
teapot.name = 'teapot'

# teapotb = OBJ('models/teapot')
# teapotb.name = 'teapot'

# teapotc = OBJ('models/teapot')
# teapotc.name = 'teapot'


print('<importing Mesh>')
from mesh import Mesh
print('<importing render>')
from render import render
print('<importing Scene>')
from scene import Scene

scene = Scene(camera=camera)
#scene.add_object( teapot )
scene.add_object( teapot )
#scene.add_object( teapotc )

teapot.rotate( 90, axis='x',local=False)

teapot.geometry_to_origin()
# teapot.origin_to_geometry()



#teapot.translate([-1,0,0])


#quit()

alert('<running loop>')



@analyze
def event_processing():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
    
@analyze
def animation():
    mag = 1 / timer.x.fps # one degree per second

    # c = time.perf_counter()
    teapot.rotate(mag * 20, axis='z',local=False)
    # d = time.perf_counter()
    # print('c->d',(d-c)*1000)
    teapot.rotate(mag*30, axis='z',local=True)
    teapot.rotate(mag*4, axis='y',local=True)



@analyze
def render_to_screen(image=None, screen=None):
    assert image and screen
    screen.blit(image, (0,0) )
    pygame.display.flip()  # Refresh on-screen display

@analyze
def application():
    """this is the stuff that determines what the scene object is"""
    event_processing()
    animation()

@analyze
def printout():
    timer.dump()

@fps
@analyze
def update():
    #clear_terminal()
    #timer.clear_buffer()
    application()
    
    image = render(screen=screen, scene=scene, scaling=config['window']['scaling'])
    
    render_to_screen(image=image, screen=screen)
    printout()

timer.dump()
while True:
    update()
    

    
    
    
    