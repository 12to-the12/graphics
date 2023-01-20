import numpy as np

def arr(x): return np.array(x)

origin = arr([ 0, 0, 0])
n_Z    = arr([ 0, 0,-1])
Y      = arr([ 0, 1, 0])

class entity:
    def __init__(self, position=origin,view_vector=n_Z,up_vector=Y):
        self.position = position
        self.view_vector = view_vector
        self.up_vector = up_vector

    def __str__(self) -> str:
        return f"view_vector: {self.view_vector}"

    def translate(self,change):
        assert change.shape == (3,), f"change should be an array with three elements, not {change.shape}"
        self.position = self.position + change