import numpy as np
from vector_math import arbitrary_axis_rotation, orthogonal, angle
from ignore import ignore
def arr(x): return np.array(x)

world_origin = arr([ 0, 0, 0])
n_Z    = arr([ 0, 0,-1])
Y      = arr([ 0, 1, 0])

class Entity:
    def __init__(self, origin=world_origin,view_vector=n_Z,up_vector=Y):
        self.origin = world_origin
        self.view_vector = view_vector
        self.up_vector = up_vector

        self.scale_factor = 1

        # these don't work, something to think about later
        #self.z_rotation = angle(ignore(self.view_vector,'z'),  Y)
        #self.y_rotation = angle(ignore(self.view_vector,'y'),  Y)
        #self.x_rotation = angle(ignore(self.view_vector,'x'),n_Z)

        

    def __str__(self) -> str:
        return f"view_vector: {self.view_vector}"

    def translate(self,change):
        assert change.shape == (3,), f"change should be an array with three elements, not {change.shape}"
        self.position = self.position + change
    
    def scale(self,factor):
        """scales in every direction equally"""
        self.scale_factor *= factor
    
    def rot_axis(self,axis,degrees):
        """rotates the entity around the given axis"""
        self.view_vector = arbitrary_axis_rotation(self.view_vector, axis, degrees)
        self.up_vector   = arbitrary_axis_rotation(self.up_vector,   axis, degrees)

    def rotate(self,degrees,local=True,axis='Z'):
        """the user accessed rotate command
        for the local rotations the view_vector acts as the Y axis, the up_vector acts as
        the Z, and the orthogonal between them acts as the X"""
        if local:
            if axis is  'X': axis = np.cross(self.view_vector,self.up_vector)
            if axis is  'Y': axis = self.view_vector
            if axis is  'Z': axis = self.up_vector
        if not local:
            X = np.array([ 1, 0, 0])
            Y = np.array([ 0, 1, 0])
            Z = np.array([ 0, 0, 1])
            if axis is 'X': axis = X
            if axis is 'Y': axis = Y
            if axis is 'Z': axis = Z
        self.rot_axis(axis, degrees)
        return axis

    # these rotations operate in camera space
    # assuming the vector is pointing towards you, 
    # counter clockwise is the positive direction of rotation
    def rotate_pitch(self,degrees):
        """ y and z, x is the vector nodding, upwards nod is positive"""
        cross = np.cross(self.view_vector,self.up_vector)
        self.up_vector   = arbitrary_axis_rotation(self.up_vector, cross, degrees)
        self.view_vector = arbitrary_axis_rotation(self.view_vector, cross, degrees)
        
    def rotate_yaw(self,degrees):
        """ x and y, z is the vector shaking head, left rotation is positive"""
        self.view_vector = arbitrary_axis_rotation(self.view_vector, self.up_vector, degrees)
    def rotate_roll(self,degrees):
        """ x and z, y is the vector side to side, indian head nod, rolling right is positive"""
        self.up_vector = arbitrary_axis_rotation(self.up_vector, self.view_vector, degrees)