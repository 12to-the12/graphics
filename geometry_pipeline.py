
from vector_math import arbitrary_axis_rotation, normal_of_polygons
from alert import alert
import numpy as np
from numpy import linalg
import numpy.typing as npt
from camera import Camera
alert('<compiling geometry_pipeline>')

def normal_cull(geometry : np.ndarray, camera : Camera) -> np.ndarray:
    """
    receives (-1, 3, 3)

    dot product of zero means perpindicular(orthogonal)
    negative means greater than 90 degrees
    positive means less than 90 degrees
    1 means parallel, -1 means perpendicular

    we only want to keep polygons with negative dot products to the camera vecotor,
    inclusive of -1

    returns (-1, 3, 3)
    """
    normals = normal_of_polygons(geometry)
    assert normals.ndim == 2, 'normals should be shaped (-1,3)'
    dot_products = linalg.multi_dot([normals, camera.view_vector])
    assert dot_products.ndim == 1, f'dot_products should be shaped (-1,) not {dot_products.shape}'
    pass_table = (dot_products < 0)
    #print(type(pass_table))
    #print('pass_table', pass_table.shape)
    #print(geometry.shape)
    filtered_geometry = geometry[pass_table]
    assert filtered_geometry.dtype == 'float64', f'{filtered_geometry.dtype}'
    return filtered_geometry

    

def project_in_camera_space(geometry : np.ndarray, camera : Camera) -> np.ndarray:
    assert geometry.dtype == 'float64', f'{geometry.dtype}'
    """
    receives (-1, 3)
    
    projects world coordinates in camera space, with the camera centered
    and facing towards -Z with the up vector towards +Y
    
    returns (-1, 3)
    """
    assert geometry.ndim == 2, f'geometry shaped bad as {geometry.shape}'
    
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
    assert geometry.dtype == 'float64', f'{geometry.dtype}'
    geometry = arbitrary_axis_rotation(geometry,axis_b,angle_b) # not inverted angles
    geometry = arbitrary_axis_rotation(geometry,axis_a,angle_a) # not inverted angles
    
    
    assert geometry.ndim == 2, f'geometry shaped bad as {geometry.shape}'
    return geometry

def z_sort(geometry: np.ndarray) -> np.ndarray:
    """
    receives (-1,3,3)

    sorts polygons by their z coordinate

    returns (-1, 3, 3)
    
    """
    assert geometry.ndim == 3, f'geometry shaped bad as {geometry.shape}'
    position = np.average(geometry, axis=1)
    assert position.ndim == 2, f'position shaped bad as {position.shape}'
    z = position[:,2]
    assert z.ndim == 1, f'z shaped bad as {z.shape}'
    indexes = z.argsort()
    #indexes = np.flip(indexes)
    sorted_geometry = geometry[indexes]

    assert sorted_geometry.ndim == 3, f'sorted_geometry shaped bad as {sorted_geometry.shape}'
    
    return sorted_geometry

def project_in_screen_space(geometry : np.ndarray, camera : Camera) -> np.ndarray:
    """
    receives (-1, 3)
    
    foreshortens with w
    also culls out of range values

    returns (-1, 3) xyw
    """
    assert geometry.ndim == 2, "geometry needs to be a table of vertexes"

    
    xyw = np.array([ 1, 1,-1])
    geometry *= xyw

    xy = geometry[ :,:2]
    w  = geometry[ :, 2]
    w = w.reshape(-1,1)
    xy = xy / w # foreshortening
    
    xy *= [camera.focal_ratio * 2, camera.focal_ratio * 2 * camera.aspect_ratio]

    xyw = np.concatenate([xy, w], axis=1)

    assert xyw.ndim == 2, f"xyw needs to be (-1,3) not {xyw.shape}"
    return xyw

def frustrum_cull(xyw, camera : Camera):
    """
    receives xyw (-1, 3)
    culls values outside of the viewing frustrum
    returns coordinates (-1, 2)
    """

    xy = xyw[ :,:2]
    w  = xyw[ :, 2]

    # cull close and far
    pass_table = (camera.close_cull <= w) & ( w <= camera.far_cull) # 1d per vector cull

    pass_table = pass_table.reshape(-1,3) # cull for every vector

    pass_table = ~np.all(~pass_table, axis=1) # culls polygon if every vector is out

    xy = xy.reshape(-1,3,2)
    xy = xy[pass_table]
    xy = xy.reshape(-1,2)

    
    # cull left right top bottom
    pass_table = (-1 <= xy) & ( xy <= 1) # this operates on a per coordinate basis
    pass_table = ~np.any( ~pass_table, axis=1) # if a vertex is out either vertically or horizontally, it's culled

    pass_table = pass_table.reshape(-1,3)
    pass_table = ~np.all( ~pass_table, axis=1) # this removes any polygon that has no visible vertexes

    xy = xy.reshape(-1,3,2)
    xy = xy[pass_table]
    xy = xy.reshape(-1,2)

    assert xy.ndim == 2, "returns coords as (-1,2)"
    return xy



def project_screen_coordinates(coordinates : np.ndarray, screen) -> np.ndarray:
    """
    receives coordinates (-1,2)
    
    scales the coordinates from [-1,1] to  the proper screen size

    returns coordinates (-1 ,2)
    """
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
    camera.origin    = np.array(( 0, 0, 0)) # x,y,z
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

    
