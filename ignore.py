import numpy as np
def ignore(vector,component):
    x,y,z = vector
    if component=='x': return np.array([0,y,z])
    if component=='y': return np.array([x,0,z])
    if component=='z': return np.array([x,y,0])