from numba import njit
import numpy as np
from vector_math import normalize



def generate_rays(x_res, y_res, z, random=False, norm=True):
    size = x_res
    start = -size/2
    end   = start + size
    x_rays = np.arange(start,end)

    size = y_res
    start = -size/2
    end   = start + size
    y_rays = np.arange(start,end)

    a, b = np.meshgrid(x_rays,y_rays)
    table = np.dstack([a,b]).reshape(-1,2) # this creates a list of coordinate pairs based on the inputted axes
    if random: table += np.random.random([y_res*x_res,2])
    out =  np.hstack([table,np.full([x_res*y_res,1],-z)])
    #print(out)
    #print(out.shape)
    #print(out.dtype)
    if norm: out = normalize(out)
    return out

    

#@njit(parallel=True)
def ray_cast(canvas=None, camera=None,objects=None,lights=None,
            world=None,samples=10,reflection_budget=0,refraction_budget=0):
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
    h_res = canvas.get_width()
    v_res = canvas.get_height()
    camera.focal_ratio
    # 2 and 2 focal ratio 1
    # multiply the two


    


    
    

if __name__ == "__main__":
    x = generate_rays(3,3,2)
    print(x)