print('<top of render>')
from ray_cast import ray_cast
import pygame
from mesh import Mesh
from geometry_pipeline import *
from object import Object
from draw import draw_points, draw_polygons
from timer import timer
print('<bottom of render>')
def render( screen=None, scene=None ):
    """a necessary layer that allows me to switch rendering methods when I want to.
    between ray tracing and conventional rendering, maybe cel shading
    
    returns a pygame surface
    """
    assert screen, 'no screen ascribed for render function'
    assert scene,  'no scene ascribed for render function'

    #canvas = pygame.Surface.copy(canvas)

    h_res, v_res = 500,500#1920/1.25,1000/1.25
    canvas = pygame.Surface((h_res, v_res))

    # this line calls ray_cast on the given scene information
    #pixel_array = ray_cast(canvas=canvas, scene=scene)
    #image = pygame.surfarray.make_surface( pixel_array )

    
    #out = draw_points(canvas=canvas, scene=scene)
    out = draw_polygons(canvas=canvas, scene=scene)
    #out =  ray_cast(canvas=canvas,scene=scene)
    out = pygame.transform.smoothscale( out, screen.get_size()  ) # transforms the outputted surface to fit the display size

    timer('drawing')
    return out
    
     