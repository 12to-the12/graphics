import numpy as np
from numba import njit
@njit(debug=True)#(float64[:](float64[:],float64[:],boolean))
def quaternion(vector,x, transpose=False): # the transpose flag flips which array is arranged vertically and which is horizontal
    # this creates a multiplicative table of the two arrays and runs them through the quaternion table
    assert vector.shape == (4,), "the given vector needs to have four elements"
    
    if transpose:
        print(vector.shape)
        vector = np.expand_dims(vector, 1)
    else:
        x = np.expand_dims(x, 1)
    
    a = 1
    print(vector.shape)

    return 1 # scalar, i ,j ,k

print(quaternion(np.array([0,7,2,5]),np.array([-0.5,0.5,0.5,0.5])))