
import bpy
import xml.etree.ElementTree as ET
from .base import BaseIO
from .mesh import MeshIO
from .material import MaterialIO
from .light import LightIO
from .integrator import IntegratorIO
from .camera import CameraIO
from .film import FilmIO
import pyzen


class SceneIO(BaseIO):
    """
    """

    def __init__(self):
        self.meshio = MeshIO()
        self.materialio = MaterialIO()
        self.lightio = LightIO()
        self.integratorio = IntegratorIO()
        self.filmio = FilmIO()
        self.cameraio = CameraIO()

    def write_description(self, handle, path):
        self.lightio.write_description(handle)

        objects_node = ET.SubElement(handle, 'Objects')
        for obj in bpy.context.scene.objects:
            if obj.hide_get():
                continue

            if obj.type == 'MESH':
                self.meshio.write_description(objects_node, obj, path)
                self.materialio.write_description(objects_node)

    def feed_api(self):
        scene = pyzen.api.Scene()

        self.integratorio.feed_api(scene)
        self.filmio.feed_api(scene)
        self.cameraio.feed_api(scene)
        
        for obj in bpy.context.scene.objects:
            if obj.hide_get():
                continue

            if obj.type == 'MESH':
                self.meshio.feed_api(scene, obj)
                self.materialio.feed_api(scene, obj)
            elif obj.type == 'LIGHT':
                self.lightio.feed_api(scene, obj)