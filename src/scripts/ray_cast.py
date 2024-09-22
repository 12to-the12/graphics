from utilities.timer import timer
import pygame
from scripts.mesh import Mesh
from scripts.geometry_pipeline import project_in_camera_space
from scripts.vector_math import normalize, norm, normal_of_polygon
import numpy as np
from numba import njit, float64, boolean, guvectorize, prange  # type: ignore
from utilities.alert import alert
from scripts.scene import Scene

# alert('<top of ray_cast>')

alert("<compiling ray_cast>")


@njit(float64(float64[:], float64[:]), cache=True)
def dot(a: np.ndarray, b: np.ndarray) -> float:
    out: float = np.sum(a * b)
    return out


@njit(float64[:](float64[:], float64[:, :]), cache=True)
def ray_plane_intersection(ray, points):
    ray_origin = np.array([0, 0, 0])
    N = normal_of_polygon(points)
    # print(f'planes normal: {N}')
    # print(f'ray:{ray}')
    # print(dot(ray, N) )
    if dot(ray, N) > 0:
        # print('the plane normal is facing away from the ray')
        return np.array([0.0, 0.0, 0.0])
    if abs(dot(ray, N)) <= 1e-4:
        # print('the plane normal and ray are at right angles, no intersection is possible')
        return np.array([0.0, 0.0, 0.0])
    C = points[0]  # any point that lies on the shared plane
    V = ray

    W = C - ray_origin
    k = dot(W, N) / dot(V, N)
    # k is the multiplier with the ray to reach I from the ray_origin
    # if the ray is a unit vector it is the distance from ray_origin to the intersection

    I = ray_origin + k * V
    # print(f'k: {k}')
    if k < 0:
        return np.array([0.0, 0.0, 0.0])  # ray is facing away from plaen
    if k == 0:
        return np.array([0.0, 0.0, 0.0])  # ray is on plane I think
    # print ('distance:',k)
    return I  # returns the intersection point


@njit(float64[:](float64[:], float64[:]), cache=True)
def project_vector(a, b):  # projects b onto a
    return (dot(a, b) / dot(a, a)) * a


# @guvectorize([float64[:], float64[:,:],boolean[:]], '(n),(n,n)->(n)', nopython=True)
@njit([boolean(float64[:], float64[:, :])], cache=True)
def ray_triangle_intersection(ray, points):
    """this function determines intersection and returns the barycentric
    coordinates of the intersection point if there is a hit"""
    # print(f'ray:{ray}')
    # print(f'points:{points}')
    # print()
    I = ray_plane_intersection(ray, points)  # the point of intersection
    # print(f'I:{I}')
    if np.all(I == 0):
        return False
    A, B, C = points

    AB = B - A
    CB = B - C
    v = AB - project_vector(CB, AB)

    AI = I - A
    # print(f'AI:{AI}')
    # a is the barycentric coordinate component, if 0, I is at A, if bigger than one, it's outside the triangle
    # print( 1 - project_vector(v, AI) / project_vector(v, AB))
    # print('v',v)
    a = 1 - (dot(v, AI) / dot(v, AB))
    # print(f'a:{a}')

    BC = C - B  # the mother line
    AC = C - A
    v = BC - project_vector(AC, BC)
    BI = I - B
    # print(f'BI:{BI}')
    # barycentric coordinate for b
    b = 1 - (dot(v, BI) / dot(v, BC))
    # print(f'b:{b}')

    CA = A - C  # motherline
    BA = A - B
    # finding the CB instead of the CA at the star of the expression took an hour
    v = CA - project_vector(BA, CA)
    CI = I - C
    # print(f'CI:{CI}')
    # barycentric coordinate for c
    # print('v',v)
    c = 1 - (dot(v, CI) / dot(v, CA))
    # print(f'c:{c}')

    barycentric_coordinates = np.array([a, b, c])
    # print(f'barycentric_coordinates:\n{barycentric_coordinates}')
    # print('\n')
    if np.any(barycentric_coordinates < 0):
        return False
    if np.any(barycentric_coordinates > 1):
        return False
    return True


@njit(boolean[:](float64[:, :], float64[:, :, :], boolean[:]), cache=True)
def intersection_loop(rays, geometry, mask):
    for index in prange(rays.shape[0]):
        for triangle in geometry:
            if ray_triangle_intersection(rays[index], triangle):
                mask[index] = True

    return mask


def generate_rays(
    x_res: int, y_res: int, z: float, random: bool = False, norm: bool = True
) -> np.ndarray:
    # print('generating rays')
    # print(f'x_res: {x_res}')
    # print(f'y_res: {y_res}')
    # print(f'z: {z}')
    size = x_res
    start = -size / 2
    end = start + size
    x_rays = np.arange(start, end)
    assert len(x_rays.shape) == 1, f"x_rays shouldn't be shaped {x_rays.shape}"
    size = y_res
    start = -size / 2
    end = start + size

    y_rays = np.arange(start, end)
    # because otherwise it would start with negative values
    y_rays = np.flip(y_rays, 0)
    assert len(y_rays.shape) == 1, f"y_rays shouldn't be shaped {y_rays.shape}"

    a, b = np.meshgrid(x_rays, y_rays)
    # this creates a list of coordinate pairs based on the inputted axes
    table = np.dstack([a, b]).reshape(-1, 2)

    if random:
        table += np.random.random([y_res * x_res, 2])
    else:
        table += 0.5
    out = np.hstack([table, np.full([x_res * y_res, 1], -z)])

    # print(f'out: {out}')
    # print(out.dtype)
    if norm:
        out = normalize(out)
    return out


# @njit(parallel=True)
def ray_cast(
    canvas: pygame.Surface,
    scene: Scene,
    samples: int = 10,
    reflection_budget: int = 0,
    refraction_budget: int = 0,
) -> pygame.Surface:
    """
    returns a numpy shape (-1,-1,3) array

    alright, THE function

    this function takes the geometry, lighting, camera, and other scene data and
    returns an image

    I'm considering a system where instead of rebuilding the geometry array from every object
    and it's own origin and orientation, changes are written to a persistent array

    loop for every sample
    loop for every bounce
    loop for every vertex
    loop for every light

    the acceleration structure I'm going with considers the bounding volums for every object in
    the scene

    """

    assert canvas, "no canvas passed for ray_cast"
    assert scene, "no scene passed for ray_cast"

    camera = scene.camera
    objects = scene.objects
    lights = scene.lights
    world = scene.world

    h_res = canvas.get_width()
    v_res = canvas.get_height()
    # 2 and 2 focal ratio 1
    # multiply the two
    # print(f'h_res {h_res}')
    # print(f'v_res {v_res}')
    # print(f'camera.focal_ratio {camera.focal_ratio}')
    rays = generate_rays(h_res, v_res, camera.focal_ratio * h_res, norm=True)
    # print(f'generated rays [4] : {rays[4]}')
    rays = rays.reshape(-1, 3)

    mesh = Mesh()
    mesh.build(scene.objects)

    geometry = project_in_camera_space(mesh.geometry.reshape(-1, 3), camera).reshape(
        -1, 3, 3
    )
    # geometry *= np.array([1,1,-1]) # don't use, thought it was necessary, it's not
    # print(f'projected geometry:{geometry}')
    # print(rays.shape)
    # print(f'rays [4] :{rays[4]}')
    mask = np.full([rays.shape[0]], False)
    # alert('<casting rays>')
    timer("projection")
    print(f"rays:\t{rays.shape}")
    print(f"geometry:\t{geometry.shape}")
    print(f"mask:\t{mask.shape}")

    mask = intersection_loop(rays, geometry, mask)

    timer("intersection")
    # alert('<done>')
    # print('mask', mask)
    mask = np.repeat(mask, 3)
    pixels = np.full([h_res * v_res, 3], 0, dtype="uint32")
    np.place(pixels.reshape(-1), mask, 255)
    pixels = pixels.reshape(-1, 3)
    # print(pixels)
    pixels = pixels.reshape(v_res, h_res, 3)
    # print(pixels.shape )
    # print(canvas.get_size())

    pixels = pixels.transpose(1, 0, 2)

    pygame.surfarray.blit_array(canvas, pixels)

    return canvas


if __name__ == "__main__":

    ray: np.ndarray = np.array([0.0, 0.0, -1.0])

    polygon: np.ndarray = np.array(
        [[4.0, -3.0, -10.0], [0.0, 2.0, -10.0], [-3.0, -1.0, -10.0]]
    )
    print()
    timer("init")
    print(ray_triangle_intersection(ray, polygon))
    timer("inter")
