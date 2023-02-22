from entity import Entity
from vector_math import arbitrary_axis_rotation
import numpy as np
from timer import timer
from numba import prange, njit
import typing
from analysis import analyze
class Scene_Object(Entity):
    """a physical object that exists in a scene to be rendered
    info about vertices, faces, textures coordinates, and normals
    material object too, maybe per face"""
    count = 0
    list =  []
    def __init__(self, geometry, name=None):
        # bounding box, source geometry, translated, shader, textures
        super().__init__()
        self.index = Scene_Object.count
        Scene_Object.count += 1

        if name: self.name=name
        else: self.name = self.index
        Scene_Object.list.append(self)

        

        
        self.source_geometry = geometry
        # following subject to transformations
        self.geometry = self.source_geometry


    def get_objects():
        return Scene_Object.list 

    def translate(self,change):

        super().translate(change)
        self.geometry += change
      

    def scale(self,factor):
        """only scales in every direction equally"""
        super().scale(factor)
        self.geometry *= factor

    @analyze
    def rotate(self,degrees,local=True,axis='Z'):
        
        axis = super().rotate(degrees,local=local,axis=axis)
        self.geometry = arbitrary_axis_rotation(self.geometry.reshape(-1,3), axis, degrees).reshape(-1,3,3)
        
    
    def origin_to_geometry(self):
        # the resulting global values should be unchanged
        center = np.average(self.geometry.reshape(-1,3),axis=0)
        shift = center-self.origin

        #print('center', center)
        #print('shift', shift)
        #print('origin', self.origin)


        self.origin = center
        
        self.geometry = self.geometry - shift

    def geometry_to_origin(self):
        center = np.average(self.geometry.reshape(-1,3),axis=0)
        shift = center-self.origin


        # self.origin = center
        
        self.geometry = self.geometry - shift
        



#@njit
def parse_obj(text):
    """this function parses a subset of features supported by obj files
    it processes the following tags: # mtllib usemtl v vt vn f

    it first builds appropriate sized array and then populates them

    can only handle triangles
    """
    prefixes   =          ['usemtl','vt','vn','v','f']
    occurences = np.array([       0,   0,   0,  0,  0])

    text = text.split('\n')
    prefix_index = 0
    prefix = prefixes[prefix_index]

    slashes = False

    # this mess of a loop finds the number of occurences for every element so a
    # properly sized array can be constructed to contain them
    for line in text:
        if line.startswith('#'): continue
        if '/' in line: slashes = True
        
        for index in range(5):
            if line.startswith(prefixes[index]):

                
                occurences[index] += 1
                continue

    usemtl = np.zeros((occurences[0]))
    usemtl_index = 1
    vt     = np.zeros((occurences[1],3))
    vt_index = 0
    vn     = np.zeros((occurences[2],3))
    vn_index = 0
    v      = np.zeros((occurences[3],3))
    v_index = 0


    f_3d       = np.empty((occurences[4],3,3))
    f       = np.empty((occurences[4],3))
    f_index = 0

    for line in text:
        if line.startswith('#'): continue
        elif line.startswith('usemtl'):
            mtl = line[7:]
        elif line.startswith('vt'):
            line = line[2:]
            vt[vt_index] = np.array(  [ float(x) for x in line.split() ])
            vt_index += 1
        elif line.startswith('vn'):
            line = line[2:]
            vn[vn_index] = np.array(  [ float(x) for x in line.split() ])
            vn_index += 1
        elif line.startswith('v'):
            line = line[1:]
            v[v_index]   = np.array(  [ float(x) for x in line.split() ])
            v_index += 1
        elif line.startswith('f'):
            line = line[1:]
            if '/' in line:
                line = line.split()
                for index in range(3):
                    numbers = line[index].split('/')
                    number = np.array(  [ float(x) for x in numbers ])
                    f_3d[f_index,index] = number
            else:
                f[f_index]   = np.array(  [ float(x) for x in line.split() ])
            f_index += 1
    f -= 1 # because their indexes start at one like idiots
    f = f.astype(np.int32)
    return [v, vt, vn, f]

                    



import time

def import_obj(filename):
    with open(filename) as file:
        text = file.read()
    #print('<start>')
    parse_obj(text)
    tic = time.time()
    out = parse_obj(text)
    toc = time.time()
    #print(f"{round((toc-tic)*1000)}ms")
    return out

#@njit(parallel=True)
def build_geometry(v, f):
    out = np.empty([f.shape[0],3,3])

    for index in range(f.shape[0]):
        face = f[index]
        for i in range(3):
            vertex = face[i]
            #print(f'i:{i}')
            #print(f'index:{index}')
            #print(f'vertex:{vertex}')
            out[index][i] = v[vertex]
    return out


class OBJ(Scene_Object):
    def __init__(self,filepath):
        self.v, self.vt, self.vn, self.f = import_obj(filepath+'.obj')
        geometry =  build_geometry(self.v, self.f)

        super().__init__(geometry=geometry)

     

if __name__ == "__main__":
    np.set_printoptions(suppress=True) # suppresses scientific notation
    v, vt, vn, f = import_obj('models/teapot.obj')

    print('v', v.shape )
    print('vt',vt.shape)
    print('vn',vn.shape)
    print('f', f.shape )
