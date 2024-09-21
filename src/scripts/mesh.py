import numpy as np
from utilities.analysis import analyze


class Mesh:
    """a mesh to be rendered"""

    def __init__(self):
        pass

    @analyze
    def build(self, objects):
        # print('\n\n')
        """generates an array of geometry given the inputted objects"""
        polygon_count = 0
        for object in objects:
            # print(object.geometry.shape[0])
            # print(object.geometry[5])
            polygon_count += object.geometry.shape[0]
        self.geometry = np.array([])
        # np.empty([len(objects),polygon_count, 3, 3])
        # print(self.geometry.shape)
        # print('polygon count:',polygon_count)
        for index, object in enumerate(objects):
            # alert(f'generating mesh for {object.name}')
            # alert(f'self.geometry {self.geometry.shape}')
            # alert(f'index {index}')
            # #alert(f'length {object.geometry.shape[0]}')
            # x = object.geometry + object.origin
            # print('x shape',x.shape)
            # print('index',index)
            # print('close index', index+object.geometry.shape[0])
            self.geometry = np.append(self.geometry, object.geometry + object.origin)

        self.geometry = self.geometry.reshape(-1, 3, 3)

        # print(self.geometry.shape)

        # print(self.geometry[6320+5])
        # print(self.geometry[6320+100])

    @analyze
    def build_vertex_list(self, objects):
        """generates a list of all vertexes in a scene. Because I want draw_points to work"""
        vertex_count = 0
        for object in objects:
            vertex_count += object.v.shape[0]
        self.v = np.empty([vertex_count, 3])

        for index, object in enumerate(objects):
            self.v[index : index + object.v.shape[0]] = object.v + object.origin
