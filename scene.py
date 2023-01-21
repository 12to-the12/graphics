from object import Object
import numpy as np
class Scene:
    def __init__(self, camera=None, objects=None, lights=None, world=None):
        self.camera = camera
        self.objects = np.array([])
        self.lights = lights
        self.world = world

    def add_object(self, object):
        self.objects = np.append(self.objects, object)