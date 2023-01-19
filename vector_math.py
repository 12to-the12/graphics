

# https://www.youtube.com/watch?v=PsBx8Kkhc5Y
# refer to for quaternion math


import numpy as np
from clear_terminal import clear_terminal
from alert import alert


def magnitude(vector):
    assert vector.shape[1] == 3, "the magnitude function takes a LIST of vectors"
    return np.sqrt(np.sum(vector**2, 1))

def normalize(vector): # operates on a list of vectors with three components a piece
    assert vector.shape[1] == 3, "the normalize function takes a LIST of vectors"
    return vector / magnitude(vector).reshape(-1,1)


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

    
    t = vectors*x
    t = t.reshape(-1,4,4)
    
    valence = [
        [ 1, 1, 1, 1],
        [ 1,-1, 1,-1],
        [ 1,-1,-1, 1],
        [ 1, 1,-1,-1]
        ]

    t = t*valence
    assert t.shape[1:] == (4,4), f"the t array is not shaped correctly, it should be a list of 4x4 matrices, not {t.shape}"

    s = t[:,0,0]+t[:,1,1]+t[:,2,2]+t[:,3,3]
    i = t[:,0,1]+t[:,1,0]+t[:,2,3]+t[:,3,2]
    j = t[:,0,2]+t[:,1,3]+t[:,2,0]+t[:,3,1]
    k = t[:,0,3]+t[:,1,2]+t[:,2,1]+t[:,3,0]

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
    out = np.transpose(np.vstack((s,i,j,k))) # this creates a list of the four elements sijk vectors
    assert out.shape[1] == 4, "the function returns a list of four elements vectors, not {out.shape}"
    return out # scalar, i ,j ,k



def arbitrary_axis_rotation(points,rotation_axis,degrees): # vector_array
    single_flag = False
    if len(points.shape) == 1:
        points = points.reshape(1,-1)
        single_flag = True
    assert points.shape[1] == 3, "the arbitrary_axis_rotation function takes a LIST of vectors"
    assert rotation_axis.shape == (3,), "the rotation axis is not correctly shaped"
    # rotation axis has to be a unit vector
    angle = np.radians(degrees)

    d,e,f = rotation_axis
    q = (  np.cos(angle/2), d*np.sin(angle/2), e*np.sin(angle/2), f*np.sin(angle/2)   )
    q = np.array(q)
    qprime = ( q[0] , q[1]*-1, q[2]*-1, q[3]*-1 ) # q prime is an inverted q, with the magnitude left alone
    qprime = np.array(qprime)
    
    zeros = np.zeros((points.shape[0])).reshape(-1,1)
    u = np.concatenate((zeros, points),axis=1)
    

    x = quaternion(u,q)
    if single_flag:
        return quaternion(x,qprime, transpose=True)[0,1:]
    return quaternion(x,qprime,transpose=True)[:,1:]

if __name__ == "__main__":
    clear_terminal()
    print('\n'*50)
    print('*'*20)
    rotation_axis = np.array([[0,0,1]])
    rotation_axis = normalize(rotation_axis)[0]

    theta = 90 # theta 240  725, returns 0257
    vectors = np.array([[7,2,5],[1,0,0],[0,1,0],[0,0,1]])
    x = arbitrary_axis_rotation(vectors,rotation_axis,theta)
    
    print(f"result:{x}")
