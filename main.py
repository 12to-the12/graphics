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



camera.translate([0,-25,0])

from models.attempt import a
from object import Scene_Object, OBJ


triangle = OBJ('models/triangle')
triangle.name = 'triangle'

cube = OBJ('models/cube')
cube.name = 'cube'

# # cat = OBJ('models/cat')
# # cat.name = 'cat'

teapot = OBJ('models/teapot')
teapot.name = 'teapot'

teapotb = OBJ('models/teapot')
teapotb.name = 'teapotb'

teapotc = OBJ('models/teapot')
teapotc.name = 'teapotc'


print('<importing Mesh>')
from mesh import Mesh
print('<importing render>')
from render import render
print('<importing Scene>')
from scene import Scene

scene = Scene(camera=camera)
scene.add_object( teapot )
scene.add_object( teapotb )
scene.add_object( teapotc )
# scene.add_object( triangle )
# scene.add_object( cube )

teapot.rotate( 90, axis='x',local=False)
teapotb.rotate( 90, axis='x',local=False)
teapotc.rotate( 90, axis='x',local=False)

teapot.geometry_to_origin()
teapotb.geometry_to_origin()
teapotc.geometry_to_origin()
# teapot.origin_to_geometry()



teapotb.translate([-5,0,0])
teapotc.translate([ 5,0,0])


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
    teapot.rotate(mag * -10, axis='z',local=False)
    teapot.rotate(mag*30, axis='z',local=True)
    teapot.rotate(mag*4, axis='y',local=True)

    teapotb.rotate(mag * 30, axis='z',local=False)
    teapotb.rotate(mag*3, axis='z',local=True)
    teapotb.rotate(mag*-2, axis='y',local=True)

    teapotc.rotate(mag * 50, axis='z',local=False)
    teapotc.rotate(mag*-70, axis='z',local=True)
    teapotc.rotate(mag*-60, axis='y',local=True)
    pass



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
    

    
    
    
    