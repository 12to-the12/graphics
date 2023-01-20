

# https://www.youtube.com/watch?v=PsBx8Kkhc5Y
# refer to for quaternion math


import numpy as np
from numba import njit
from clear_terminal import clear_terminal
from alert import alert
from timer import timer
from numba import jit, njit, int32, float64
from numba import int32, float64, i4, f8, boolean
from numba import prange

@njit(float64(float64[:]))
def magnitude(vector):
    #assert vector.shape[1] == 3, "the magnitude function takes a LIST of vectors"
    return np.sqrt(np.sum(vector**2))


@njit(float64[:](float64[:]))
def normalize(vector): # operates on a list of vectors with three components a piece
    #assert vector.shape[1] == 3, "the normalize function takes a LIST of vectors"
    return vector / magnitude(vector)

@njit(float64[:](float64[:],float64[:]))
def orthogonal(a, b):
    """returns the normalize orthogonal to the inputted vectors"""
    #a = np.round(a, 10)
    #b = np.round(b, 10)
    #assert a.shape == (3,), "a needs to be a vector"
    #assert b.shape == (3,), "b needs to be a vector"

    if np.all(a == b): raise Exception(f"given vectors are identical")
    if not np.any(np.cross(a,b)): raise Exception(f"no orthogonal between diametrically opposed vectors")
    
    return normalize(np.cross(a,b) )

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



@njit(float64[:](float64[:],float64[:],boolean) )
def quaternion(vector,x, transpose=False):
    # the transpose flag flips which array is arranged vertically and which is horizontal
    # this creates a multiplicative table of the two arrays and runs them through the quaternion table
    assert vector.shape == (4,), "the given vector needs to have four elements"
    x2 = np.expand_dims(x, 1)
    t = vector*x2
    if transpose:
        
        t = np.transpose(t)
    
        
    
    #print(vector.shape)
    #print(x.shape)
    #print(vector)
    #print(x)
    #
    #print(t)

    valence = np.array([
        [ 1., 1., 1., 1.],
        [ 1.,-1., 1.,-1.],
        [ 1.,-1.,-1., 1.],
        [ 1., 1.,-1.,-1.]
        ])
    
    t = t*valence
    #assert t.shape[1:] == (4,4), f"the t array is not shaped correctly, it should be a list of 4x4 matrices, not {t.shape}"

    s = t[ 0, 0]+t[ 1, 1]+t[ 2, 2]+t[ 3, 3]
    i = t[ 0, 1]+t[ 1, 0]+t[ 2, 3]+t[ 3, 2]
    j = t[ 0, 2]+t[ 1, 3]+t[ 2, 0]+t[ 3, 1]
    k = t[ 0, 3]+t[ 1, 2]+t[ 2, 1]+t[ 3, 0]

    """
    the previous coordinate summations implements the following quaternion table,
    with the negativity table accounting for the valence
    x    1  i  j  k  
      _____________
    1|  +1  i  j  k
    i|   i -1  k -j
    i|   j -k -1  i
    k|   k  j -i -1

    """
    
    return np.array([s,i,j,k]) # scalar, i ,j ,k


@njit(float64[:,:](float64[:,:],float64[:],float64),parallel=True)
def arbitrary_axis_rotation(points,rotation_axis,degrees): # vector_array
    assert points.shape[1] == 3, "the arbitrary_axis_rotation function takes a LIST of vectors"
    assert rotation_axis.shape == (3,), "the rotation axis is not correctly shaped"
    
    # rotation axis has to be a unit vector
    rotation_axis = normalize(rotation_axis)
    
    angle = np.radians(degrees)

    d,e,f = rotation_axis
    cosine = np.cos(angle/2)
    sine   = np.sin(angle/2)
    q = ( cosine, d*sine, e*sine, f*sine )
    q = np.array(q)
    qprime = ( q[0] , q[1]*-1, q[2]*-1, q[3]*-1 ) # q prime is an inverted q, with the magnitude left alone
    qprime = np.array(qprime)
    
    len = points.shape[0]
    out = np.ones((len,3),dtype='float64')
    
    for index in prange(len):
        u = np.concatenate((np.array([0.]), points[index] ) )
        x = quaternion(u,q,transpose=False)
        x = quaternion(x,qprime,transpose=True)[1:]
        out[index] = x
    
    return out




@njit()
def speed(vectors,rotation_axis,theta):
    out = arbitrary_axis_rotation(vectors,rotation_axis,theta)
if __name__ == "__main__":
    clear_terminal()
    print('\n'*50)
    print('*'*20)


    
    rotation_axis = np.array( [ 1., 1., 1.] )
    rotation_axis = normalize(rotation_axis)

    theta = 240 # theta 240  725, returns 0257
    theta == np.float64(theta)
    vectors = np.array([[ 7., 2., 5.]])
    
    print(vectors)

    timer('start')
    x = arbitrary_axis_rotation(vectors,rotation_axis,theta)
    
    print(f"result:{x}")
    timer('first run')
    vectors = np.random.randint(10,size=(1_000_000,3))
    vectors = vectors.astype('float64')
    timer('build array')
    arbitrary_axis_rotation(vectors,rotation_axis,theta)
    timer('time')
    
    
