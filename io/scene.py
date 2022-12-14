
import bpy
import xml.etree.ElementTree as ET
from .base import BaseIO
from .mesh import MeshIO
from .material import MaterialIO
from .light import LightIO


class SceneIO(BaseIO):
    """
    """

    def __init__(self):
        self.meshio = MeshIO()
        self.materialio = MaterialIO()
        self.lightio = LightIO()

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
        self.lightio.feed_api()
        
        for obj in bpy.context.scene.objects:
            if obj.hide_get():
                continue

            if obj.type == 'MESH':
                self.meshio.feed_api()
                self.materialio.feed_api()