import numpy as np
from alert import alert

class Mesh:
    """a mesh to be rendered"""
    def __init__(self):
        pass

    def build(self, objects):
        """generates an array of geometry given the inputted objects"""
        polygon_count = 0
        for object in objects:
            polygon_count += object.geometry.shape[0]
        self.geometry = np.empty([polygon_count, 3, 3])

        for index, object in enumerate(objects):
            alert(f'generating mesh for {object.name}')
            alert(f'self.geometry {self.geometry.shape}')
            alert(f'index {index}')
            alert(f'length {object.geometry.shape[0]}')
            self.geometry[index:index+object.geometry.shape[0]] = object.geometry
        print(f'the mesh generated is of the shape {self.geometry.shape}')
    