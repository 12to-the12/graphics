from ray_cast import ray_cast
import pygame


def render(  canvas=None, camera=None, geometry=None, lights=None, world=None):
    """a necessary layer that allows me to switch rendering methods when I want to.
    between ray tracing and conventional rendering, maybe cel shading
    
    operates in place, returns nothing
    """
    # this line calls ray_cast on the given scene information
    pixel_array = ray_cast(canvas=None, camera=None,objects=None,lights=None,world=None)
    image = pygame.surfarray.make_surface( pixel_array )
     