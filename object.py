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
        self.geometry = arbitrary_axis_rotation(self.geometry, axis, degrees)
    
    def origin_to_geometry(self):
        center = np.average(self.geometry,axis=0)
        self.geometry -= center
        self.origin = center


from numba import njit
@njit  
def build_blocks(text):
    prefixes =          ['v ','vt','vn','f ']
    start    = np.array([  0,   0,   0,  0])
    length   = np.array([  0,   0,   0,  0])

    text = text.split('\n')
    prefix_index = 0
    prefix = prefixes[prefix_index]
    for line in text:
        if line.startswith(prefix): length[prefix_index] += 1
        if items[0] == 'v': print(items)



def import_obj(filename):
    with open(filename) as file:
        text = file.read()
    
    build_blocks(text)

if __name__ == "__main__":
    import_obj('teapot.obj')