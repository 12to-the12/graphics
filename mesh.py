import numpy as np

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
            #alert(f'generating mesh for {object.name}')
            #alert(f'self.geometry {self.geometry.shape}')
            #alert(f'index {index}')
            #alert(f'length {object.geometry.shape[0]}')
            self.geometry[index:index+object.geometry.shape[0]] = object.geometry + object.origin
        self.geometry = self.geometry.reshape(-1, 3, 3)
    
    def build_vertex_list(self, objects):
        """generates a list of all vertexes in a scene. Because I want draw_points to work"""
        vertex_count = 0
        for object in objects:
            vertex_count += object.v.shape[0]
        self.v = np.empty([vertex_count, 3])

        for index, object in enumerate(objects):
            self.v[index:index+object.v.shape[0]] = object.v + object.origin


    