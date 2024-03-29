import os
import bpy
import xml.etree.ElementTree as ET
from .base import BaseIO
from .mesh import MeshIO
from .material import MaterialIO
from .light import LightIO
from .integrator import IntegratorIO
from .camera import CameraIO
from .film import FilmIO
from .. import pyzen


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

        lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../shader'))
        scene.set_shader_search_path(lib_path)
        
        for obj in bpy.context.scene.objects:
            if obj.hide_get():
                continue

            if obj.type == 'MESH':
                self.meshio.feed_api(scene, obj)
                self.materialio.feed_api(scene, obj)
            elif obj.type == 'LIGHT':
                self.lightio.feed_api(scene, obj)
                self.materialio.feed_api(scene, obj)

        scene.build_bvh()

        return scene

    def get_output_path(self):
        return getattr(self.filmio.get_props(), 'output', './output.png')