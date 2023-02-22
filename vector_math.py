from alert import alert
alert('<top of vector_math>')

import numpy as np
from clear_terminal import clear_terminal

from analysis import analyze
from numba import njit, float64, f8, i4, prange, boolean

alert('<compiling vector_math>')



def orthogonal(a, b):
    """returns the normalize orthogonal to the inputted vectors"""
    a = np.round(a, 10)
    b = np.round(b, 10)
    assert a.shape == (3,), "a needs to be a vector"
    assert b.shape == (3,), "b needs to be a vector"
    if np.all(a == b): assert False, f"no orthogonal between {a} and {b}"
    if not np.any(np.cross(a,b))  : assert False, f"no orthogonal between diametrically opposed vectors"
    
    return norm(np.cross(a,b) )

#@njit([f8[:](f8[:], f8[:])], cache=True)
def angle(a, b):
    """returns the minimum angle between two vectors expressed as degrees"""
    assert a.shape == (3,), "a needs to be a vector"
    assert b.shape == (3,), "b needs to be a vector"
    if np.all(a == b): return 0
    
    dot_product = np.dot(a,b)
    dot_product = round(dot_product,10)
    angle = np.arccos(dot_product)
    angle = np.degrees(angle)
    return angle

''''
@njit([f8[:,:](f8[:,:], f8[:])], cache=True)
def angles(polygons, vector):
    """
    
    """
    polygon_cout = polygons.shape[0]
    out = np.empty( (polygon_cout,3 )  )

    for index in polygon_cout:
        out = angle(polygon_cout, vector)

    return out
'''


    
    
@njit(cache=True)
def mag(vector):
    assert vector.shape[0] == 3, "the magnitude function takes a LIST of vectors"
    return np.sqrt(np.sum(vector**2))

@njit(cache=True)
def magnitude(vector):
    assert vector.shape[1] == 3, "the magnitude function takes a LIST of vectors"
    return np.sqrt(np.sum(vector**2, 1))

@njit(cache=True)
def norm(vector): # operates on a single vector
    assert vector.shape[0] == 3, "the normalize function takes a SINGLE vector"
    return vector / mag(vector)

#@njit(float64[:,:](float64[:,:]) )
def normalize(vectors): # operates on a list of vectors with three components a piece
    assert vectors.shape[1] == 3, "the normalize function takes a LIST of vectors"
    return vectors / magnitude(vectors).reshape(-1,1)

@njit(float64[:](float64[:,:]), cache=True)
def normal_of_polygon(points):
    """this function finds the normal of a polygon, assuming the points are wound counter clockwise"""
    a, b, c = points
    vector_a = b-a
    vector_b = c-a
    normal = np.cross(vector_a, vector_b)
    normal = norm(normal)
    return normal

@njit(float64[:,:](float64[:,:,:]), cache=True)
def normal_of_polygons(polygons):
    poly_count = polygons.shape[0]
    out = np.empty( (poly_count, 3) )
    for index in range(poly_count):
        out[index] = normal_of_polygon( polygons[index] )
    return out

alert('<compiling reshape>')
@njit([f8[:,:](i4[:], i4, i4), f8[:,:](i4[:,:], i4, i4), f8[:,:](i4[:,:,:], i4, i4),
       f8[:,:](f8[:], i4, i4), f8[:,:](f8[:,:], i4, i4), f8[:,:](f8[:,:,:], i4, i4) ], cache=True)
def reshape(array, a, b):
    """replacement for numpy's reshape while compiling with numba
    takes either a one dimensional array, two dimensional array, or three dimensional array
    returns a two dimensional array"""
    #assert np.prod(array.shape) == a * b, f"cannot reshape to {a, b}"
    if a == -1: a = int( array.size / b )
    if b == -1: b = int( array.size / a )

    array = array.flatten()
    out = np.empty((a, b))
    for i in prange(a):
        out[i] = array[i*b:i*b+b]
    return out

alert('<compiling reshape3d>')
@njit([f8[:,:,:](f8[:], i4, i4), f8[:,:,:](f8[:,:], i4, i4), f8[:,:,:](f8[:,:,:], i4, i4) ], cache=True)
def reshape3d(array, b, c):
    """this is a bespoke function for the quaternion operation that assumes that the first
    dimension needs to be inferred, and only takes the 2nd and 3rd as input"""
    #assert np.prod(array.shape) == a * b, f"cannot reshape to {a, b}"
    items = array.size
    a = items / (b * c)
    a = int(a)
    array = array.flatten()
    out = np.empty((a, b, c))
    for i in range(a):
        for j in range(b):
            out[i,j] = array[(j+i*b)*c:(j+i*b)*c+c]
    return out

alert('<compiling quaternion>')
@njit([float64[:,:](float64[:,:],float64[:],boolean)], cache=True)
def quaternion(vectors,x, transpose=False):
    """the transpose flag flips which array is arranged vertically and which is horizontal
    this function creates a multiplicative table of the two arrays and runs them through
     the quaternion table
     
     takes vectors as (-1,4) and x as (4,)"""
    assert vectors.shape[1] == 4, "the shape of vectors should be (-1,4)"
    assert x.shape == (4,), "the shape of x should be (4,)"

    #x = x.reshape(4,1)
    x = reshape(x, 4, 1)
    #vectors = vectors.reshape(-1,1,4)
    vectors = reshape3d(vectors, 1, 4)

    #print(vectors.shape)
    #print(vectorsb.shape)
    #print(np.all(vectors ==  vectorsb))

    t = vectors*x
    if transpose: t = np.transpose(t, (0, 2, 1) ) # transposes each vector operation, leaving the list of them in the right order
    

    assert t.shape[1:] == (4,4), "the t array is not shaped correctly, it should be a list of 4x4 matrices"

    s = t[:,0,0]-t[:,1,1]-t[:,2,2]-t[:,3,3]
    i = t[:,0,1]+t[:,1,0]+t[:,2,3]-t[:,3,2]
    j = t[:,0,2]-t[:,1,3]+t[:,2,0]+t[:,3,1]
    k = t[:,0,3]+t[:,1,2]-t[:,2,1]+t[:,3,0]
    
    """
    the ^previous coordinate summations implements the following quaternion table
    x    1  i  j  k  
      _____________
    1|  +1  i  j  k
    i|   i -1  k -j
    i|   j -k -1  i
    k|   k  j -i -1
    """
    
    out = np.stack( (s,i,j,k) , axis=1)
    
    # outputs an array of (s i j k) vectors, shape (-1,4)
    assert out.ndim == 2, "outputs an array of (s i j k) vectors"
    assert out.shape[1] == 4, "the function returns a list of four element vectors"
    
    return out # scalar, i ,j ,k

alert('<compiling arbitrary_axis_rotation>')



@njit([ f8[:,:](f8[:,:],f8[:],f8)], cache=True)
def arbitrary_axis_rotation(points,rotation_axis,degrees): # vector_array
    """currently, THE function it currently operate at around one million operations for
    all below 10,000, and around two million for anything up to ten million beyond that"""

    assert points.ndim == 2, "the arbitrary_axis_rotation function operates on a 2 dimensional list"
    assert points.shape[1] == 3, "the arbitrary_axis_rotation function takes a LIST of vectors"
    assert rotation_axis.shape == (3,), "the rotation axis is not correctly shaped"
    
    rotation_axis = norm(rotation_axis)
    #print(f"normalized axis: {rotation_axis}")
    # rotation axis has to be a unit vector
    angle = np.radians(degrees)

    d,e,f = rotation_axis
    sin = np.sin(angle/2)
    q = (  np.cos(angle/2), d*sin, e*sin, f*sin   )
    q = np.array(q)
    qprime = ( q[0] , q[1]*-1, q[2]*-1, q[3]*-1 ) # q prime is an inverted q, with the magnitude left alone
    qprime = np.array(qprime)
    
    zeros = np.zeros((points.shape[0])) # .reshape(-1,1)
    zeros = reshape(zeros, -1, 1)

    u = np.concatenate((zeros, points),axis=1)
    
    #timer('pre calc')
    x = quaternion(u,q, transpose=False)
    #timer('quaternion')
    
    out = quaternion(x,qprime,transpose=True)[:,1:]

    #timer('quaternion b')

    return out

alert('<compiling single__axis_rotation>')
@njit(cache=True)
def single__axis_rotation(points, rotation_axis, degrees):
    points = points.astype('float64')
    rotation_axis = rotation_axis.astype('float64')
    points = reshape(points, 1, -1)
    return arbitrary_axis_rotation(points,rotation_axis,degrees)[0]


import time
if __name__ == "__main__":
    print('__main__')

    clear_terminal()
    
    rotation_axis = np.array( [ 1., 1., 1.])
    rotation_axis = norm(rotation_axis)
    theta = 240. # theta 240  725, returns 0257
    #theta == np.float64(theta)
    vectors = np.array([[ 7., 2., 5.]])
    
    x = arbitrary_axis_rotation(vectors,rotation_axis,theta)

    rotation_axis = np.random.randint(1,10,size=(3)).astype('float64')
    vectors = np.random.randint(10,size=(1000,3)).astype('float64')
    tic = time.time()
    arbitrary_axis_rotation(vectors,rotation_axis,theta)
    toc = time.time()

    print('<start>\n')

    for size in [10_000, 100_000, 1_000_000, 10_000_000]: # ten million seems to be the scalable limit
        rotation_axis = np.random.randint(1,10,size=(3)).astype('float64')
        vectors = np.random.randint(10,size=(size,3)).astype('float64')

        tic = time.time()
        arbitrary_axis_rotation(vectors,rotation_axis,theta)
        toc = time.time()
        print(f"{round((toc-tic)*1000)}ms\tat {size} vectors")
        print(f"{round(size/(toc-tic)/1000)}k operations per second\n")

    print('<end>')