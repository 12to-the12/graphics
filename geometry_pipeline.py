
from vector_math import arbitrary_axis_rotation
from alert import alert
import numpy as np

alert('<compiling geometry_pipeline>')

def project_in_camera_space(geometry, camera):
    """projects world coordinates in camera space, with the camera centered
    and facing towards -Z with the up vector towards +Y"""
    assert len(geometry.shape) == 2, f"geometry should be  a LIST of vertexes not shape {geometry.shape}"
    assert geometry.shape[1] == 3, "geometry should be a list of vertexes"
    # at this point in the pipeline all the geometry is defined relative to the world origin
    # now, we make it relative to the camera, both the coordinates and the rotation

    # step one is easy, subtract the camera position from every world coordinate

    geometry = geometry-camera.origin

    # the second step is more difficult

    # this is where the inverse of the view transformation is performed
    # the world will be oriented with the camera pointeed straight down,
    # with the view vector towards -Z and the up vector towards +Y
    
    axis_a, angle_a, axis_b, angle_b = camera.orient()
    #alert(axis_a, angle_a, axis_b, angle_b)
    geometry = arbitrary_axis_rotation(geometry,axis_b,angle_b) # not inverted angles
    geometry = arbitrary_axis_rotation(geometry,axis_a,angle_a) # not inverted angles
    
    return geometry

def project_in_screen_space(geometry, camera):
    """projects camera space coordinates in eye space"""
    assert geometry.shape[1] == 3, "geometry needs to be a table of points"
    #alert(geometry)
    xyw = np.array([ 1, 1,-1])
    geometry *= xyw
    xy = geometry[ :,:2]
    w  = geometry[ :, 2]
    #alert(f"xy:{xy}")
    #alert(f"w:{w}")
    xy /= w.reshape(-1,1)
    #alert(f"xy:{xy}")
    #alert([camera.focal_ratio, camera.focal_ratio * camera.aspect_ratio])
    xy *= [camera.focal_ratio * 2, camera.focal_ratio * 2 * camera.aspect_ratio] # half height
    #alert(f"xy:{xy}")
    
    # cull close and far
    pass_table = (camera.close_cull <= w) & ( w <= camera.far_cull)
    xy = xy[pass_table]
    
    #alert('culling')
    # cull left right top bottom
    pass_table = (-1 <= xy) & ( xy <= 1)
    pass_table = ~np.any( ~pass_table, axis=1)
    xy = xy[pass_table]
    #alert(f"xy:{xy}")

    return xy

def project_screen_coordinates(coordinates, screen):
    h_res = screen.get_width()
    v_res = screen.get_height()

    coordinates *= [ 1,-1]
    coordinates *= 0.5
    coordinates += 0.5

    coordinates *= [h_res, v_res]
    return coordinates
    
if __name__ == "__main__":
    alert('<initializing camera>')
    from camera import Camera
    camera = Camera()
    camera.position    = np.array(( 0, 0, 0)) # x,y,z
    camera.view_vector = np.array(( 0, 1, 0))
    camera.up_vector   = np.array(( 0, 0, 1))

    alert('<rotating camera>')
    camera.rotate_yaw(0) # left
    camera.rotate_pitch(0) # up
    camera.rotate_roll(0) #

    alert('<initializing geometry>')
    geometry = np.array([[-2,2,1],[-4,2,0],[2,2,0]])

    alert('<projecting geometry>')

    geometry = project_in_camera_space(geometry, camera)
    geometry = project_in_screen_space(geometry, camera)

    
