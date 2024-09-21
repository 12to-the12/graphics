#!/usr/bin/env python3.10.9
from utilities.clear_terminal import clear_terminal

clear_terminal()
from utilities.alert import alert

from utilities.config import config, config_dict
from utilities.timer import t, fps
import utilities.timer as timer
from utilities.analysis import analyze


import numpy as np

np.set_printoptions(suppress=True)  # suppresses scientific notation

alert("<initializing pygame>")
import pygame

pygame.init()
h_res = config.window.h_res
v_res = config.window.v_res
clock = pygame.time.Clock()

# flags = pygame.FULLSCREEN | pygame.DOUBLEBUF
flags = pygame.DOUBLEBUF

screen = pygame.display.set_mode((h_res, v_res), flags)

screen.set_alpha(None)
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
# def __init__(self, aspect_ratio=1., focal_length=10, sensor_width=10, close_cull=0.1, far_cull=1000): # 23.5


from scripts.attempt import a

from scenes.teapots import teapot_scene, animation

teapot_scene = teapot_scene(config)


alert("<running loop>")


@analyze
def event_processing():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit


@analyze
def render_to_screen(image=None, screen=None):
    assert image and screen
    screen.blit(image, (0, 0))
    pygame.display.flip()  # Refresh on-screen display


@analyze
def application():
    """this is the stuff that determines what the scene object is"""
    event_processing()
    animation(teapot_scene, timer)


@analyze
def printout():
    timer.dump()


print("<importing render>")
from scripts.render import render


@fps
@analyze
def update():
    # clear_terminal()
    # timer.clear_buffer()
    application()

    image = render(screen=screen, scene=teapot_scene, scaling=config.window.scaling)

    render_to_screen(image=image, screen=screen)
    printout()


timer.dump()

if __name__ == "__main__":
    while 1:
        update()
