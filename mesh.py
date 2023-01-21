import numpy as np

class Mesh:
    """a mesh to be rendered"""
    def __init__(self):
        pass

    def build(self, objects):
        """generates an array of geometry given the inputted objects"""
        self.geometry = np.array([])
        for object in objects:
            self.geometry = np.append(self.geometry, object.geometry).reshape(-1,3)
    