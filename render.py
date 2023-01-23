print('<top of render>')
from ray_cast import ray_cast
import pygame
from mesh import Mesh
from geometry_pipeline import *
from object import Object
from draw_points import draw_points
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

    h_res, v_res = 100,100#1920/1.25,1000/1.25
    canvas = pygame.Surface((h_res, v_res))

    # this line calls ray_cast on the given scene information
    #pixel_array = ray_cast(canvas=canvas, scene=scene)
    #image = pygame.surfarray.make_surface( pixel_array )

    
    
    out =  ray_cast(canvas=canvas,scene=scene)
    out = pygame.transform.scale( out, [200,200])
    print(out)
    timer('drawing')
    return out
    
     