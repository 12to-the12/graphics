
from geometry_pipeline import *
from mesh import Mesh
import pygame
from analysis import analyze
from config import config
import random, time

@analyze
def draw_points(canvas=None, scene=None):
    """a simple renderer that plots vertexes as points on the canvas
    
    returns the canvas"""

    assert canvas, 'no canvas for draw_points'
    assert scene,   'no scene for draw points'
    canvas.fill("white")  # Fill the display with a solid color
    camera = scene.camera


    mesh = Mesh()
    mesh.build_vertex_list(scene.objects)
    assert len(mesh.v.shape) == 2, f"the vertex list should be a list of vertexes not shape {mesh.v.shape}"

    geometry = project_in_camera_space(mesh.v, camera)
    
    coords   = project_in_screen_space(geometry, camera)
    coords   = project_screen_coordinates(coords, canvas)

    for coord in coords:
        pygame.draw.circle(canvas, (0,0,0), coord, 1)


    return canvas

h_res = config['window']['h_res']
v_res = config['window']['v_res']
scaling = config['window']['scaling']
dimensions = np.array(([h_res, v_res]))

occlusion = config['raster']['occlusion']
individual = config['raster']['individual']
width = config['raster']['weight'] # line weight
# else: width = 0

draw_color = config['raster']['draw_color']
face_color = config['raster']['face_color']
background = config['raster']['background']



@analyze
def loop(coords=None, canvas=None, width=None):
    assert not coords is None, 'coords not defined'
    assert not canvas is None, 'canvas not defined'
    assert not width is None, 'no width specified'

    screen = pygame.display.get_surface()
    
    for coord in coords:
        if occlusion:
            pygame.draw.polygon(canvas, face_color, coord, 0)

        pygame.draw.polygon(canvas, draw_color, coord, width)

        if individual:
            # out = pygame.transform.scale(canvas, (h_res, v_res) )
            screen.blit(canvas, (0,0) )
            pygame.display.flip()


@analyze
def draw_polygons(canvas=None, scene=None, individual=False):
    """a simple renderer that draws polygons either as solids or as a wireframe

    kind of inefficient, as it draws every polygon rather than every line segment
    
    returns the same canvas"""

    assert canvas, 'no canvas for draw_points'
    assert scene,   'no scene for draw points'
    
    camera = scene.camera

    

    canvas.fill( background ) # Fill the display with a solid color
    mesh = Mesh()
    mesh.build(scene.objects)
    # print(mesh.geometry.shape)
    # print(mesh.geometry[6320+450])
    # print(mesh.geometry[6320+100])
    # print(mesh.geometry[6320+0])
    # print(mesh.geometry[6320+1])

    
    geometry = mesh.geometry
    if occlusion: geometry = normal_cull(geometry, camera)
    
    geometry = geometry.reshape(-1, 3)

    assert geometry.dtype == 'float64', f'{geometry.dtype}'
    geometry = project_in_camera_space(geometry, camera)
    assert geometry.ndim == 2, f'geo badly shaped as {geometry.shape}'

    
    

    if occlusion:
        geometry = z_sort(geometry.reshape(-1,3,3) ).reshape(-1,3)

    xyw = project_in_screen_space(geometry, camera)

    coords = frustrum_cull(xyw, camera)
    
    
    assert coords.ndim == 2, f'coords badly shaped as {coords.shape}'
    
    coords = project_screen_coordinates(coords, canvas)


    coords = coords.reshape(-1,3,2)
    
    

    loop(coords=coords, canvas=canvas, width=width)
    



    return canvas
