
from geometry_pipeline import *
from mesh import Mesh
import pygame
from timer import timer

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
    geo = project_in_camera_space(mesh.v, camera)
    timer('camera projecting')
    coords   = project_in_screen_space(geo, camera)
    timer('screen projecting')
    coords   = project_screen_coordinates(coords, canvas)
    timer('coord projecting')

    for coord in coords:
        pygame.draw.circle(canvas, (0,0,0), coord, 1)

    timer('drawing')

    return canvas

def draw_polygons(canvas=None, scene=None):
    """a simple renderer that draws polygons either as solids or as a wireframe

    kind of inefficient, as it draws every polygon rather than every line segment
    
    returns the canvas"""

    assert canvas, 'no canvas for draw_points'
    assert scene,   'no scene for draw points'
    canvas.fill("white")  # Fill the display with a solid color
    timer('in draw_points')
    camera = scene.camera


    mesh = Mesh()
    mesh.build(scene.objects)

    geo = project_in_camera_space(mesh.geometry.reshape(-1,3), camera)
    timer('camera projecting')
    coords   = project_in_screen_space(geo, camera)
    timer('screen projecting')
    coords   = project_screen_coordinates(coords, canvas).reshape(-1,3,2)
    timer('coord projecting')

    for coord in coords:
        pygame.draw.polygon(canvas, (0,0,0), coord, 1)

    timer('drawing')

    return canvas
