
from geometry_pipeline import *
from mesh import Mesh
import pygame
from timer import timer
import time
def draw_points(canvas=None, scene=None):
    """a simple renderer that plots vertexes as points on the canvas
    
    returns the canvas"""

    assert canvas, 'no canvas for draw_points'
    assert scene,   'no scene for draw points'
    canvas.fill("white")  # Fill the display with a solid color
    timer('in draw_points')
    camera = scene.camera


    mesh = Mesh()
    mesh.build_vertex_list(scene.objects)
    assert len(mesh.v.shape) == 2, f"the vertex list should be a list of vertexes not shape {mesh.v.shape}"
    timer('building')
    geometry = project_in_camera_space(mesh.v, camera)
    timer('camera projecting')
    
    coords   = project_in_screen_space(geometry, camera)
    timer('screen projecting')
    coords   = project_screen_coordinates(coords, canvas)
    timer('coord projecting')

    for coord in coords:
        pygame.draw.circle(canvas, (0,0,0), coord, 1)

    timer('drawing')

    return canvas

def draw_polygons(canvas=None, scene=None, wireframe=True, solid=True):
    """a simple renderer that draws polygons either as solids or as a wireframe

    kind of inefficient, as it draws every polygon rather than every line segment
    
    returns the canvas"""

    assert canvas, 'no canvas for draw_points'
    assert scene,   'no scene for draw points'
    canvas.fill("white")  # Fill the display with a solid color
    
    camera = scene.camera

    canvas.fill( (0, 0, 0) )
    mesh = Mesh()
    mesh.build(scene.objects)

    
    geometry = mesh.geometry
    geometry = normal_cull(geometry, camera)

    geometry = geometry.reshape(-1, 3)

    assert geometry.dtype == 'float64', f'{geometry.dtype}'
    geometry = project_in_camera_space(geometry, camera)
    timer('camera projecting')
    assert geometry.ndim == 2, f'geo badly shaped as {geometry.shape}'

    
    

    if solid:
        geometry = z_sort(geometry.reshape(-1,3,3) ).reshape(-1,3)
    timer('z_sort')

    xyw = project_in_screen_space(geometry, camera)
    timer('screen space')

    coords = frustrum_cull(xyw, camera)


    
    assert coords.ndim == 2, f'coords badly shaped as {coords.shape}'
    
    coords = project_screen_coordinates(coords, canvas)
    coords = coords.reshape(-1,3,2)
    timer('screen projecting')
    if wireframe: width = 1
    else: width = 0

    
    for coord in coords:
        if solid: pygame.draw.polygon(canvas, (0,0,0), coord, 0)
        pygame.draw.polygon(canvas, (0,255,0), coord, width)
        pygame.display.flip()
        screen = pygame.display.get_surface()
        screen.blit(canvas, (0,0) )
        #time.sleep(0.1)


    timer('drawing')

    return canvas
