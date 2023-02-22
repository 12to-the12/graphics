print('<top of render>')
from ray_cast import ray_cast
import pygame
from mesh import Mesh
from geometry_pipeline import *
from object import Scene_Object
from draw import draw_points, draw_polygons
from timer import timer, t
from tree import tree
from analysis import analyze
from config import config
print('<bottom of render>')



    
h_res = config['window']['h_res']
v_res = config['window']['v_res']
scaling = config['window']['scaling']
dimensions = np.array(([h_res, v_res]))
assert type(h_res) == int, print(type(h_res))
assert type(v_res) == int, print(type(v_res))
assert type(scaling) == int or float, print(type(scaling))



@analyze
def scale(canvas):
    if config["window"]["smoothscale"]:
        return pygame.transform.smoothscale(canvas, (h_res, v_res) ) # canvas, target
    else:
        return pygame.transform.scale(canvas, (h_res, v_res) ) # canvas, target


@analyze
def render( screen=None, scene=None , scaling=1):
    """a necessary layer that allows me to switch rendering methods when I want to.
    between ray tracing and conventional rendering, maybe cel shading
    
    returns a pygame surface
    """
    assert screen, 'no screen ascribed for render function'
    assert scene,  'no scene ascribed for render function'

    #canvas = pygame.Surface.copy(canvas)
    #h_res, v_res = np.array(screen.get_size() ) * scaling

    # yes, it needs to be here
    canvas = pygame.Surface(dimensions * scaling)

    # this line calls ray_cast on the given scene information
    #
    
    if config['render_method'] == 'points':
        canvas = draw_points(canvas=canvas, scene=scene)
    elif config['render_method'] == 'polygons':
        canvas = draw_polygons(canvas=canvas, scene=scene)
    elif config['render_method'] == 'ray_cast':
        canvas = ray_cast(canvas=canvas, scene=scene)
    else:
        raise Exception('config configured incorrectly, invalid render_method')
     
    canvas = scale( canvas ) # transforms the outputted surface to fit the display size

    return canvas
    
     