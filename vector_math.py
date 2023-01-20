
# https://www.youtube.com/watch?v=PsBx8Kkhc5Y
# refer to for quaternion math


import numpy as np
from clear_terminal import clear_terminal
from alert import alert
from timer import timer
from numba import njit, float64

def orthogonal(a, b):
    """returns the normalize orthogonal to the inputted vectors"""
    a = np.round(a, 10)
    b = np.round(b, 10)
    assert a.shape == (3,), "a needs to be a vector"
    assert b.shape == (3,), "b needs to be a vector"
    if np.all(a == b): assert False, f"no orthogonal between {a} and {b}"
    if not np.any(np.cross(a,b))  : assert False, f"no orthogonal between diametrically opposed vectors"
    
    return norm(np.cross(a,b) )

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
    
@njit
def mag(vector):
    assert vector.shape[0] == 3, "the magnitude function takes a LIST of vectors"
    return np.sqrt(np.sum(vector**2))

@njit
def magnitude(vector):
    #assert vector.shape[1] == 3, "the magnitude function takes a LIST of vectors"
    return np.sqrt(np.sum(vector**2, 1))

@njit
def norm(vector): # operates on a single vector
    assert vector.shape[0] == 3, "the normalize function takes a SINGLE vector"
    return vector / mag(vector)

@njit
def normalize(vectors): # operates on a list of vectors with three components a piece
    assert vectors.shape[1] == 3, "the normalize function takes a LIST of vectors"
    return vectors / magnitude(vectors)

def quaternion(vectors,x, transpose=False): # the transpose flag flips which array is arranged vertically and whihc is horizontal
    # this creates a multiplicative table of the two arrays and runs them through the quaternion table
    assert vectors.shape[1] == 4, f"the shape of vectors should be (-1,4) not {vectors.shape}"
    assert x.shape == (4,), f"the shape of x should be (4) not {x.shape}"
    count = vectors.shape[0] # this is the number of vectors being processed
    if transpose:
        vectors = vectors.reshape(-1,4,1)
        x = np.tile(x,[count]).reshape(count,1,4)# (4,) to (2,1,4)
    else:
        x = x.reshape(4,1)
        x = np.tile(x,[count,1]).reshape(count,4,1)
        vectors = vectors.reshape(-1,1,4)

    timer('q reshape')
    t = vectors*x
    timer('q mult     ')
    t = t.reshape(-1,4,4)
    

    assert t.shape[1:] == (4,4), f"the t array is not shaped correctly, it should be a list of 4x4 matrices, not {t.shape}"

    s = t[:,0,0]-t[:,1,1]-t[:,2,2]-t[:,3,3]
    i = t[:,0,1]+t[:,1,0]+t[:,2,3]-t[:,3,2]
    j = t[:,0,2]-t[:,1,3]+t[:,2,0]+t[:,3,1]
    k = t[:,0,3]+t[:,1,2]-t[:,2,1]+t[:,3,0]
    timer('q filter')
    """
    the ^previous coordinate summations implements the following quaternion table
    x    1  i  j  k  
      _____________
    1|  +1  i  j  k
    i|   i -1  k -j
    i|   j -k -1  i
    k|   k  j -i -1
    """
    out = np.transpose(np.vstack((s,i,j,k))) # this creates a list of the four elements sijk vectors
    timer('q transpose')
    assert out.shape[1] == 4, "the function returns a list of four elements vectors, not {out.shape}"
    return out # scalar, i ,j ,k



def arbitrary_axis_rotation(points,rotation_axis,degrees): # vector_array
    single_flag = False
    if len(points.shape) == 1:
        points = points.reshape(1,-1)
        single_flag = True
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
    
    zeros = np.zeros((points.shape[0])).reshape(-1,1)
    u = np.concatenate((zeros, points),axis=1)
    
    timer('pre calc')
    x = quaternion(u,q)
    timer('quaternion')
    if single_flag:
        return quaternion(x,qprime, transpose=True)[0,1:]
    return quaternion(x,qprime,transpose=True)[:,1:]

import time
if __name__ == "__main__":
    print('__main__')

    clear_terminal()
    
    rotation_axis = np.array( [ 1., 1., 1.])
    rotation_axis = norm(rotation_axis)
    theta = 240 # theta 240  725, returns 0257
    theta == np.float64(theta)
    vectors = np.array([[ 7., 2., 5.]])
    
    x = arbitrary_axis_rotation(vectors,rotation_axis,theta)

    rotation_axis = np.random.randint(1,10,size=(3))
    vectors = np.random.randint(10,size=(1000,3))
    vectors = vectors.astype('float64')
    tic = time.time()
    arbitrary_axis_rotation(vectors,rotation_axis,theta)
    toc = time.time()

    print('<start>\n')

    for size in [1000, 10_000, 100_000, 1_000_000, 10_000_000]: # ten million seems to be the scalable limit
        rotation_axis = np.random.randint(1,10,size=(3))
        vectors = np.random.randint(10,size=(size,3))
        vectors = vectors.astype('float64')

        tic = time.time()
        arbitrary_axis_rotation(vectors,rotation_axis,theta)
        toc = time.time()
        print(f"{round((toc-tic)*1000)}ms\tat {size} vectors")
        print(f"{round(size/(toc-tic)/1000)}k operations per second\n")

    print('<end>')