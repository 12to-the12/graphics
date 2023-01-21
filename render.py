from ray_cast import ray_cast
import pygame
from mesh import Mesh
from geometry_pipeline import *
from object import Object
from draw_points import draw_points
from timer import timer

def render( canvas=None, scene=None ):
    """a necessary layer that allows me to switch rendering methods when I want to.
    between ray tracing and conventional rendering, maybe cel shading
    
    returns a pygame surface
    """
    assert canvas, 'no screen ascribed for render function'
    assert scene,  'no scene ascribed for render function'

    canvas = pygame.Surface.copy(canvas)

    # this line calls ray_cast on the given scene information
    #pixel_array = ray_cast(canvas=canvas, scene=scene)
    #image = pygame.surfarray.make_surface( pixel_array )

    
    
    out =  draw_points(canvas,scene=scene)
    timer('drawing')
    return out
    
     