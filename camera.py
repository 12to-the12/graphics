
import numpy as np
from vector_math import arbitrary_axis_rotation, normalize
from vector_math import orthogonal, angle
from ignore import ignore
from clear_terminal import clear_terminal
from alert import alert


class Camera():
    def __init__(self):
        pass
    def __str__(self) -> str:
        return f"camera view_vector: {self.view_vector}"
    def translate(self,change):
        assert change.shape == (3), f"change should be an array with three elements, not {change.shape}"
        self.position = self.position + change


    def orient(self):


        """finds the orientation of the camera in relation to -Z expressed
        as a series of cardinal rotations
        Z   = np.array([ 0., 0., 1.]) #  Z
        n_Z = np.array([ 0., 0.,-1.]) # -Z
        Y   = np.array([ 0., 1., 0.]) # +Y
        X   = np.array([ 1., 0., 0.]) # +X

        alert(f"view_vector: {camera.view_vector}")
        alert(f"up_vector:   {camera.up_vector}")


        angle_a = 0
        flat = ignore(self.view_vector,'z')
        if np.any(flat):
            alert(f"flat: {flat}")
            flat = normalize(flat)
            alert(f"flat: {flat}")
            angle_a = angle(flat,Y)
            alert(self.up_vector)
            valence_a = 1
        if angle_a == 180:
            yz_view_vector = arbitrary_axis_rotation(self.view_vector,Y,180)
            yz_up_vector   = arbitrary_axis_rotation(self.up_vector,Y,180)
        elif angle_a != 0: # this all only happens if angle_a is not zero
            axis_a = orthogonal(flat,Y)
            alert(f"axis_a:  {axis_a}")
            valence_a = axis_a[2]

            yz_view_vector = arbitrary_axis_rotation(self.view_vector,axis_a,angle_a)
            yz_up_vector   = arbitrary_axis_rotation(self.up_vector,axis_a,angle_a)
        else:
            valence_a = 1
            yz_view_vector = camera.view_vector
            yz_up_vector   = camera.up_vector
        alert(f"yz_view_vector: {yz_view_vector}")
        alert(f"yz_up_vector:   {yz_up_vector}")
        # no X discrepancy now

        # now for the second operation
        alert('ack')
        
        angle_b = angle(yz_view_vector,n_Z)
        alert(f"angle_b: {angle_b}")
        alert(yz_view_vector)
        
        if angle_b == 180:
            valence_b = 1
            z_view_vector = arbitrary_axis_rotation(yz_view_vector,X,180)
            z_up_vector   = arbitrary_axis_rotation(yz_up_vector,X,180)
        elif angle_b > 0: # only computed if theres something to compute
            axis_b = orthogonal(yz_view_vector,n_Z)

            
            alert(f"axis_b:  {axis_b}")
            valence_b = axis_b[0]



            z_view_vector = arbitrary_axis_rotation(yz_view_vector,axis_b,angle_b)
            z_up_vector   = arbitrary_axis_rotation(yz_up_vector,axis_b,angle_b)
            
        else:
            valence_b = 1
            z_view_vector = yz_view_vector
            z_up_vector   = yz_up_vector
        alert(f"z_view_vector: {z_view_vector}")
        alert(f"z_up_vector:   {z_up_vector}")
        # no Y either discrepancy now, it should be pointing straight down, just twisted around Z
        
        angle_c = angle(z_up_vector, Y)
        alert(f"angle_c: {angle_c}")
        if angle_c == 180:
            valence_c = 1
            final_up_vector = arbitrary_axis_rotation(z_up_vector,n_Z,180)
        elif angle_c > 0:
            axis_c = orthogonal(z_up_vector, Y)

            alert(f"axis_c:  {axis_c}")
            valence_c = axis_c[2]

            final_up_vector   = arbitrary_axis_rotation(z_up_vector,axis_c,angle_c)
        else:
            valence_c = 1
            final_up_vector = z_up_vector
        alert('')
        alert(f"z_view_vector:{z_view_vector}")
        alert(f"final_up_vector:  {final_up_vector}")

        Y_rotation = angle_a * valence_a
        alert(f"Y rotation: {Y_rotation}")

        X_rotation = angle_b * valence_b
        alert(f"X rotation: {X_rotation}")

        Z_rotation = angle_c * valence_c
        alert(f"Z rotation: {Z_rotation}")

        running_view_vector = arbitrary_axis_rotation(z_view_vector,       Y, -Y_rotation)
        running_view_vector = arbitrary_axis_rotation(running_view_vector, X, -X_rotation)
        running_view_vector = arbitrary_axis_rotation(running_view_vector, Z, -Z_rotation)
        print()
        print(running_view_vector)
        print(self.view_vector)
        
        running_up_vector = arbitrary_axis_rotation(final_up_vector,   Y, -Y_rotation)
        running_up_vector = arbitrary_axis_rotation(running_up_vector, X, -X_rotation)
        running_up_vector = arbitrary_axis_rotation(running_up_vector, Z, -Z_rotation)
        print(running_up_vector)
        print(self.up_vector)

        return np.array([Z_rotation,X_rotation,Y_rotation])

    """


    # these rotations operate in camera space
    # assuming the vector is pointing towards you, 
    # counter clockwise is the positive direction of rotation
    def rotate_pitch(self,degrees):
        # y and z, x is the vector
        # nodding, upwards nod is positive
        
        cross = np.cross(self.view_vector,self.up_vector)
        self.up_vector   = arbitrary_axis_rotation(self.up_vector, cross, degrees)
        self.view_vector = arbitrary_axis_rotation(self.view_vector, cross, degrees)
        
    def rotate_yaw(self,degrees):
        # x and y, z is the vector
        # shaking head, left rotation is positive
        self.view_vector = arbitrary_axis_rotation(self.view_vector, self.up_vector, degrees)
    def rotate_roll(self,degrees):
        # x and z, y is the vector
        # side to side, indian head nod, rolling right is positive
        self.up_vector = arbitrary_axis_rotation(self.up_vector, self.view_vector, degrees)
    

if __name__ == "__main__":
    np.set_printoptions(suppress=True) # suppresses scientific notation
    clear_terminal()
    camera = Camera()
    camera.position    = np.array(( 0,-1, 0)) # x,y,z
    camera.view_vector = np.array(( 0, 1, 0))
    camera.up_vector   = np.array(( 0, 0, 1))

    

    

    for x in [-180,0,180,360,50]:
        camera.rotate_yaw(x) # left
        camera.rotate_pitch(x) # up
        camera.rotate_roll(x) # up

        camera.orient()