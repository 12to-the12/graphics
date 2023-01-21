from entity import Entity
from vector_math import arbitrary_axis_rotation
import numpy as np
from timer import timer

class Object(Entity):
    """a physical object that exists in a scene to be rendered
    info about vertices, faces, textures coordinates, and normals
    material object too, maybe per face"""
    count = 0
    list =  []
    def __init__(self, geometry=None, name=None):
        # bounding box, source geometry, translated, shader, textures
        super().__init__()
        self.index = Object.count
        Object.count += 1

        if name: self.name=name
        else: self.name = self.index
        Object.list.append(self)

        
        self.source_geometry = geometry
        # following subject to transformations
        self.geometry = self.source_geometry

    def get_objects():
        return Object.list   

    def scale(self,factor):
        """only scales in every direction equally"""
        super().scale(factor)
        self.geometry *= factor

    def rotate(self,degrees,local=True,axis='Z'):
        axis = super().rotate(degrees,local=local,axis=axis)
        timer('rotate')
        self.geometry = arbitrary_axis_rotation(self.geometry, axis, degrees)
    
    def origin_to_geometry(self):
        center = np.average(self.geometry,axis=0)
        self.geometry -= center
        self.origin = center
        print(center)
    